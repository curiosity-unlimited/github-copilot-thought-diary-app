# Thought Diary App
- A full-stack web application powered by AI that allows users to write [Thought Diaries](https://positivepsychology.com/thought-diary/), which help identify & challenge negative thinking patterns, promoting healthier mental habits.
- A demo app from the course - GitHub Copilot

## Features
- Two approaches are provided in this course to implement the app: **"advanced-workflow"** and **"master-workflow"**.
    - We'll start with **"advanced-workflow"** to implement the app in order to demonstrate more ways to interact with GitHub Copilot Chat.
        - The workflow has `advanced-workflow-start` and `advanced-workflow-end` branches.
    - Then we'll switch to **"master-workflow"** to implement the app again to show how top-level implementation with GitHub Copilot Chat looks like.
        - The workflow has `master-workflow-start` and `master-workflow-end` branches.
- Please follow the instructions in the **"Setup"** section below to set up your local development environment.

## Setup
1. Fork the repository: 
- Please follow [GitHub Docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) to fork the repository to your GitHub account.
- **IMPORTANT: Please uncheck the "Copy the DEFAULT branch only" option when forking in order to copy all branches into the new fork.**
2. Clone the repository from your GitHub account:
- Please replace `<your-github-username>` with your GitHub account username in the command below:
    ```
    git clone https://github.com/<your-github-username>/github-copilot-thought-diary-app.git
    cd github-copilot-thought-diary-app
    ```

3. Fetch all the branches:
    ```
    git fetch --all
    ```

4. List all the branches and make sure `advanced-workflow-start`, `advanced-workflow-end`, `master-workflow-start`, and `master-workflow-end` are in the list:
    ```
    git branch -a
    ```

5. Switch to one of the following branches:
- Switch to the `advanced-workflow-start` branch, which marks the beginning of **"advanced-workflow"** implementation. If you want to follow along with the course step-by-step, please switch to this branch and start from there:
    ```
    git checkout advanced-workflow-start
    ```

- Switch to the `advanced-workflow-end` branch, which marks the end of **"advanced-workflow"** implementation. If you want to take a look at the completed application, please switch to this branch.
    ```
    git checkout advanced-workflow-end
    ```

- Switch to the `master-workflow-start` branch, which marks the beginning of **"master-workflow"** implementation. If you want to follow along with the course step-by-step, please switch to this branch and start from there. 
    ```
    git checkout master-workflow-start
    ```

- Switch to the `master-workflow-end` branch, which marks the end of **"master-workflow"** implementation. If you want to take a look at the completed application, please switch to this branch.
    ```
    git checkout master-workflow-end
    ```

6. Checkout a specific commit or step if necessary:
- Please replace `<commit-hash>` with the specific commit hash:
    ```
    git checkout <commit-hash>
    ```

## License

[MIT](LICENSE)
