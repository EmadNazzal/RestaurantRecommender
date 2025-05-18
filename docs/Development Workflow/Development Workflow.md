# Development Workflow

## 1. Setup Environment

### Steps

1. Install Node.js dependencies by running the following command in the root directory of the project:
    ```bash
    npm install
    ```
2. Create and activate a virtual environment by running the following command in the root directory of the project:
    ```bash
    conda create --name nibbler python=3.11
    conda activate nibbler
    ```
3. Navigate to the `backend` directory and install Python dependencies by running the following commands:
    ```bash
    cd apps/backend
    pip install -r requirements.txt
    ```
4. Install pre-commit hooks by running the following command:
    ```bash
    pre-commit install
    ```
5. Modify the `mypy` executable path in the `.vscode/settings.json` file to match the path on your system. Also adjust any of the optional sections to match your preferences.
6. Install VS Code Extensions:
    - [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
    - [HTMLHint](https://marketplace.visualstudio.com/items?itemName=mkaufman.HTMLHint)
    - [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
    - [Mypy](https://marketplace.visualstudio.com/items?itemName=ms-pyright.pyright)
    - [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
    - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Ruff](https://marketplace.visualstudio.com/items?itemName=QBB.ruff)
    - [Shell Script Command Completion](https://marketplace.visualstudio.com/items?itemName=foxundermoon.shell-format) (Optional)
    - [Shellcheck](https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck) (Optional)
    - [shfmt](https://marketplace.visualstudio.com/items?itemName=foxundermoon.shell-format) (Optional)
    - [SonarLint](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode)
    - [Spell Right](https://marketplace.visualstudio.com/items?itemName=ban.spellright)
    - [Stylelint](https://marketplace.visualstudio.com/items?itemName=stylelint.vscode-stylelint)

## 2. Create Development Branch

### Standards

- Use the following branch naming convention: `<identifier>-<title>`.
    - The `<identifier>` is the task ID of the Linear task you want to work on, with the `<title>` referring to the task title.
    - Example: `ID-123-add-login-button`.
        <details>
        <summary>How to Find and Copy the Branch Name</summary>

        - When viewing the task in Linear, press the button highlighted in the screenshot below to copy the `<identifier>-<title>` to your clipboard.

            ![Linear Branch Name Screenshot][Linear Branch Name Screenshot]

        - Alternatively, you can use the shortcut `⌘ + ⇧ + .` (Mac OS) to copy the `<identifier>-<title>` to your clipboard.
        </details>
- Do not combine multiple tasks in a single branch. Create a separate branch for each task.

### Steps

1. **Open the Task in Linear**: Open the task in Linear that you want to work on.
2. **Copy the Branch Name**: Copy the branch name from the task in Linear.
3. **Create a New Branch**: Create a new branch from the `main` branch with the copied branch name.
    ```bash
    git checkout -b <branch-name>
    ```
    - Example:
        ```bash
        git checkout -b ID-123-add-login-button
        ```

## 3. Develop Feature

### Standards

- Follow the standards for the language you are working with. The standards can be found in the [Languages Standards Folder].
- Provide detailed comments in the code.
- Provide detailed documentation comments in the code, following the style guide for the language you are working with as outlined in the [Languages Standards Folder].
- Use `TODO` comments to mark todos and action items in the code, using the format `TODO(username): action item`, with the username referring to your GitHub username.
- Use the provided configuration files to ensure code quality.

## 4. Commit Changes Throughout Development

### Standards

- Make small, incremental commits.
- Use the following commit message format:
    ```bash
    <type>: short description

    Longer description here if necessary.
    ```
- See [Commit Message Convention] for more details.

### Steps

1. **Stage Changes**: Stage the changes you want to commit.
    ```bash
    git add .
    ```
2. **Commit Changes (Option 1)**: Commit the changes with a descriptive message.
    ```bash
    git commit -m "<type>: short description"
    ```
    - Example:
        ```bash
        git commit -m "feat: add html for login button"
        ```
3. **Commit Changes (Option 2)**: Use [cz-git] to easily create a commit message in the correct format. You will be led through a series of prompts to create the commit message.
    ```bash
    npx cz
    ```

## 5. Rebase Changes

### Standards

- Use `git rebase` to keep the commit history clean and concise.

### Steps

1. **Fetch Upstream Changes**: Fetch the latest changes from the `main` branch.
    ```bash
    git fetch upstream
    ```
2. **Rebase Branch**: Rebase the branch on the `main` branch.
    ```bash
    git rebase upstream/main
    ```
3. **Resolve Conflicts**: Resolve any conflicts that arise during the rebase.

## 6. Run Tests

### Standards

- Run the tests for the project to ensure the changes do not break existing functionality.
- Update or add tests as necessary.
- Ensure the tests pass before pushing the changes.

### Steps

1. **Update Tests**: Update or add tests as necessary.
2. **Run Tests**: Run the tests for the project.

    > TO DO: Add steps for running tests.

## 7. Push Changes with Pre-push Checks

### Standards

- [Pre-commit] hooks are used as pre-push checks to ensure code quality.
- These are run automatically when you try to push changes to the remote repository.
- If the checks fail, fix the issues and commit the changes again.

### Steps

1. **Push Changes**: Push the changes to the remote repository.
    ```bash
    git push origin <branch-name>
    ```
    - Example:
        ```bash
        git push origin ID-123-add-login-button
        ```
2. **Fix Issues**: If the push fails due to issues with the pre-commit hooks, fix the issues and commit the changes again.

## 8. Create Pull Request

### Standards

- Use the following pull request title format: `<issue type>: short description (<closing type> ID-<number>)`.
    - See [Pull Request Convention] for more details.
- The pull request template must be filled out with the necessary information.
    - See [Pull Request Template] for more details.
- The CI/CD will automatically run tests and checks on the pull request.

### Steps

1. **Create Pull Request**: Create a pull request from the branch to the `main` branch.
2. **Fill Out Pull Request Template**: Fill out the pull request template with the necessary information.
3. **Submit Pull Request**: Submit the pull request.
4. **Run CI/CD Pipeline**: The CI/CD pipeline will run the tests and checks.
    - If the pipeline fails, fix the issues and push the changes to the branch. The pipeline will run again.

## 9. Review Changes

### Standards

- After the pipeline passes, a reviewer can provide feedback on the changes.
- [Conventional Comments] are used to provide feedback on the code.

### Steps (Developer)

1. **Address Comments**: Address any comments or suggestions made by the reviewer.
2. **Push Changes**: Push the changes to the branch.
    ```bash
    git add .
    git commit
    git push origin <branch-name>
    ```
3. **Review Changes**: Wait for the reviewer to review the changes.
4. **Merge Changes**: Once the reviewer approves the changes, the reviewer will merge the pull request into the `main` branch.
5. **Deployment**: The changes will be deployed to the production environment by the CI/CD pipeline.
6. **Close Task**: The task should be automatically closed in Linear.

### Steps (Reviewer)

1. **Review Changes**: Review the changes made in the pull request.
2. **Provide Feedback**: Provide feedback using [Conventional Comments].
3. **Approve Changes**: Approve the changes if they meet the standards.
4. **Merge Changes**: Merge the pull request into the `main` branch.
5. **Deployment**: The changes will be deployed to the production environment by the CI/CD pipeline.

[Languages Standards Folder]: 3.%20Coding%20Standards/README.md
[Linear Branch Name Screenshot]: assets/LinearBranchName.png
[Commit Message Convention]: 4.%20Commit%20Messages/Commit%20Message%20Convention.md
[cz-git]: https://cz-git.qbb.sh/
[Pre-commit]: https://pre-commit.com/
[Pull Request Convention]: 8.%20Pull%20Request/Pull%20Request%20Convention.md
[Pull Request Template]: 8.%20Pull%20Request/PULL_REQUEST_TEMPLATE.md
[Conventional Comments]: 9.%20Review%20Changes/Conventional%20Comments.md
