
# Git Tracker
Git Commit & Project Explorer is a Python-based automation tool that helps you manage and commit changes in your development projects. It scans a specified bootcamp directory for projects, categorizing them as:

- **Updated:** Git repositories that are clean (no pending changes).
- **Uncommitted:** Git repositories with uncommitted or untracked changes.
- **No Git:** Directories not under Git version control.

 When you double-click on a Git-managed project, a popup appears with a default commit message. You can edit the message if needed and then commit your changes directly through the GUI.

## Features

- **Recursive Scanning:**  
  Traverses your bootcamp folder (supporting nested projects) while ignoring directories like `node_modules`, `__pycache__`, `.venv`, and `.idea`.

- **Status Categories:**  
  Projects are classified into three categories:
  - **Updated:** Git repositories with no pending changes.
  - **Uncommitted:** Git repositories with uncommitted changes.
  - **No Git:** Directories that are not under Git version control.

- **Graphical Interface:**  
  Uses Tkinter with a `ttk.Notebook` widget to create tabs for each project status. Each tab displays a list of projects with the relevant status.

- **Commit Popup:**  
  For Git repositories (Updated or Uncommitted), a double-click opens a popup window where a default commit message is shown. You can modify the message and commit changes directly from the popup window.

- **Terminal Fallback:**  
  (Optional) If a project is not under Git, the tool notifies you to initialize a repository

## Requirements

- Python 3.6 or higher
- Tkinter (Usually bundled with Python on most systems)
- Git (Command-line Git must be installed and accessible via the system PATH)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies:**

   For this project, there are no external Python libraries to install beyond the standard library. Ensure that Git is installed on your system.

## Usage

1. **Launch the Application:**

   Run the script using Python:

   ```bash
   python git_commit_explorer.py
   ```

2. **Select Your Bootcamp Folder:**

   - Click the **Browse** button at the top to choose the base folder (e.g., your `bootcamp` directory) which contains all your projects.
   - Click **Refresh** to scan the directory. The tool will then populate three tabs:
     - **Updated:** Lists Git repositories that have no pending changes.
     - **Uncommitted:** Lists Git repositories with uncommitted changes.
     - **No Git:** Lists directories that are not under Git version control.

3. **Committing Changes:**

   - In either the **Updated** or **Uncommitted** tab, double-click on a project entry.
   - A popup window appears showing the project path and a default commit message.
   - Edit the commit message if necessary and click **Commit**. The application will stage all changes and commit them using your message.
   - A success message or an error message will be displayed accordingly.

4. **For Projects Not Under Git:**

   - A double-click on a project in the **No Git** tab will show an informational popup advising you to initialize a Git repository.

## Customization

- **Ignored Directories:**  
  Update the `IGNORED_DIRS` set in the script to add or remove directories you want to skip during scanning.

- **Default Commit Message:**  
  Change the default commit message in the popup by modifying the `commit_message_var` in the `open_commit_popup` function.

- **Terminal Launch (Optional):**  
  Although the primary action is to open a commit popup, you can modify or extend the functionality (see `open_terminal_at` function) to launch your preferred terminal for additional actions.

## Contributing

Feel free to fork and improve the project. Pull requests, bug reports, and feature requests are welcome!

## License

This project is available under the [MIT License](LICENSE).

---

This README should provide enough context for users to understand, use, and customize the Git Commit & Project Explorer tool. Adjust details (like repository URL or license) as needed for your own project. Enjoy automating your Git workflow!
