import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

IGNORED_DIRS = {'node_modules', '__pycache__', '.venv', '.idea'}

def check_git_status(directory):
    """
    Check if 'directory' is a Git repository.
    Returns:
      - "Uncommitted Changes": if there are pending changes.
      - "Updated": if the repository is clean.
    """
    git_dir = os.path.join(directory, '.git')
    if os.path.isdir(git_dir):
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, cwd=directory
            )
            status_output = result.stdout.strip()
            if status_output:
                return "Uncommitted Changes"
            else:
                return "Updated"
        except Exception as e:
            return f"Error checking Git: {e}"
    return "Not Under Git"

def scan_projects(base_path):
    """
    Scans base_path recursively and separates projects into three categories:
      - Updated: Git repos with no pending changes.
      - Uncommitted: Git repos that have uncommitted changes.
      - No Git: Directories not under Git control.
    Skips directories listed in IGNORED_DIRS.
    Returns three lists of tuples: (project_path, status)
    """
    updated_projects = []
    uncommitted_projects = []
    no_git_projects = []
    
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        
        if '.git' in dirs:
            status = check_git_status(root)
            dirs[:] = []
            if status == "Updated":
                updated_projects.append((root, status))
            elif status == "Uncommitted Changes" or status.startswith("Error"):
                uncommitted_projects.append((root, status))
        else:
            no_git_projects.append((root, "Not Under Git"))
    
    return updated_projects, uncommitted_projects, no_git_projects

def open_commit_popup(project_path):
    """
    Opens a popup window where the default commit message is shown.
    You can edit the message and click Commit to add all changes and commit them.
    """
    popup = tk.Toplevel(root)
    popup.title("Commit Changes")
    popup.geometry("400x150")
    
    tk.Label(popup, text=f"Project: {project_path}", wraplength=380).pack(pady=5)
    tk.Label(popup, text="Commit Message:").pack(pady=(10, 0))
    
    commit_message_var = tk.StringVar(value="Default commit message")
    entry = tk.Entry(popup, textvariable=commit_message_var, width=50)
    entry.pack(pady=5)
    entry.focus_set()
    
    def commit():
        message = commit_message_var.get().strip()
        if not message:
            messagebox.showwarning("Warning", "Commit message cannot be empty.")
            return
        try:
            subprocess.run(["git", "add", "-A"], cwd=project_path, check=True)
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=project_path,
                capture_output=True, text=True
            )
            if result.returncode == 0:
                messagebox.showinfo("Commit", f"Commit successful:\n{result.stdout}")
            else:
                messagebox.showerror("Commit Error", f"An error occurred:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Error committing changes:\n{e}")
        popup.destroy()
    
    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)
    
    commit_button = tk.Button(btn_frame, text="Commit", command=commit)
    commit_button.pack(side=tk.LEFT, padx=20)
    cancel_button = tk.Button(btn_frame, text="Cancel", command=popup.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=20)

def open_terminal_at(directory):
    """
    Opens a new terminal window at the specified directory.
    (This function is kept for reference and is used for projects that are not Git repositories.)
    """
    try:
        if sys.platform.startswith('win'):
            subprocess.Popen(['start', 'cmd', '/K', f'cd /d {directory}'], shell=True)
        elif sys.platform.startswith('linux'):
            subprocess.Popen(['gnome-terminal', '--working-directory', directory])
        elif sys.platform.startswith('darwin'):
            apple_script = f'''
                tell application "Terminal"
                    do script "cd {directory}"
                    activate
                end tell
            '''
            subprocess.Popen(['osascript', '-e', apple_script])
        else:
            messagebox.showerror("Error", "Platform not supported for terminal launch.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not open terminal:\n{e}")


def refresh_list():
    base_path = folder_var.get()
    if not base_path or not os.path.isdir(base_path):
        messagebox.showerror("Error", "Please select a valid bootcamp directory.")
        return

    updated_list.delete(0, tk.END)
    uncommitted_list.delete(0, tk.END)
    no_git_list.delete(0, tk.END)
    
    updated_projects, uncommitted_projects, no_git_projects = scan_projects(base_path)
    
    for proj, status in updated_projects:
        entry = f"{proj}  [{status}]"
        updated_list.insert(tk.END, entry)
    
    for proj, status in uncommitted_projects:
        entry = f"{proj}  [{status}]"
        uncommitted_list.insert(tk.END, entry)
        
    for proj, status in no_git_projects:
        entry = f"{proj}  [{status}]"
        no_git_list.insert(tk.END, entry)

def on_project_select(event, listbox):
    """
    When an item is double-clicked, if it's a Git repository (Updated or Uncommitted)
    open the commit popup. If it's not under Git, alert the user.
    """
    selection = listbox.curselection()
    if selection:
        entry_text = listbox.get(selection[0])
        project_path, status_part = entry_text.split("  [", 1)
        status = status_part.rstrip("]")
        if status == "Not Under Git":
            messagebox.showinfo("Info", "This project is not under Git.\nPlease initialize a repository first.")
        else:
            open_commit_popup(project_path)

def choose_folder():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_var.set(selected_folder)
        refresh_list()

root = tk.Tk()
root.title("Git Commit & Project Explorer")
root.geometry("900x500")

folder_frame = tk.Frame(root)
folder_frame.pack(pady=10, padx=10, fill=tk.X)

folder_var = tk.StringVar()
folder_entry = tk.Entry(folder_frame, textvariable=folder_var, width=50)
folder_entry.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)
browse_button = tk.Button(folder_frame, text="Browse", command=choose_folder)
browse_button.pack(side=tk.LEFT)
refresh_button = tk.Button(folder_frame, text="Refresh", command=refresh_list)
refresh_button.pack(side=tk.LEFT, padx=(5, 0))

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

updated_tab = tk.Frame(notebook)
uncommitted_tab = tk.Frame(notebook)
no_git_tab = tk.Frame(notebook)

notebook.add(updated_tab, text="Updated")
notebook.add(uncommitted_tab, text="Uncommitted")
notebook.add(no_git_tab, text="No Git")

def create_listbox(tab):
    frame = tk.Frame(tab)
    frame.pack(expand=True, fill='both')
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    lb = tk.Listbox(frame, width=100, height=20, yscrollcommand=scrollbar.set)
    lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=lb.yview)
    return lb

updated_list = create_listbox(updated_tab)
uncommitted_list = create_listbox(uncommitted_tab)
no_git_list = create_listbox(no_git_tab)

updated_list.bind('<Double-Button-1>', lambda e: on_project_select(e, updated_list))
uncommitted_list.bind('<Double-Button-1>', lambda e: on_project_select(e, uncommitted_list))
no_git_list.bind('<Double-Button-1>', lambda e: on_project_select(e, no_git_list))

root.mainloop()

