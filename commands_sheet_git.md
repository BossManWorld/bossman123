# Git Commands Cheat Sheet

## Setup (run once)
git config --global user.name "YourName"
git config --global user.email "you@example.com"
git config --list                          # verify config

## Starting a Repo
git init                                   # init new repo
git clone https://github.com/user/repo    # copy remote repo

## Daily Workflow
git status                                 # ALWAYS run this first
git add file.txt                           # stage one file
git add .                                  # stage everything
git commit -m "describe what changed"      # save snapshot
git push                                   # send to GitHub
git pull                                   # get latest from GitHub

## Viewing History
git log --oneline                          # compact commit history
git log --oneline -5                       # last 5 commits
git diff                                   # unstaged changes
git diff --staged                          # staged changes

## Branching
git branch                                 # list branches (* = current)
git branch feature-login                   # create new branch
git switch feature-login                   # switch to branch
git switch -c feature-login                # create AND switch
git switch main                            # go back to main
git push origin feature-login             # push branch to GitHub

## Merging
git switch main
git merge feature-login                    # merge branch into main
git branch -d feature-login               # delete merged branch

## Undoing
git restore filename                       # discard changes (working tree)
git restore --staged filename             # unstage a file
git reset --soft HEAD~1                   # undo last commit, keep changes
git reset --hard HEAD~1                   # undo last commit, DELETE changes
git merge --abort                          # cancel an in-progress merge

## Resolving Merge Conflicts (step by step)
# 1. Open the conflicted file
# 2. Find the markers:
#    <<<<<<< HEAD
#    your version
#    =======
#    incoming version
#    >>>>>>> branch-name
# 3. Delete ALL three marker lines, keep the correct code
# 4. Save the file
git add conflicted-file.txt
git commit -m "resolve merge conflict"

## Remote
git remote add origin https://github.com/user/repo.git
git remote -v                              # show connected remotes
git push -u origin main                   # first push + set upstream
git push                                   # after first push, just this
git pull                                   # get + merge remote changes
git fetch                                  # get remote changes WITHOUT merging

## .gitignore (create before first commit)
__pycache__/
*.pyc
.env
*.log
venv/
.DS_Store
