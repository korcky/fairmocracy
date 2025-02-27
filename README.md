# How To

Most (if not all) of the information will be relevant to all the contributors, though cmd commands will be provided for Linux/Mac (Windows contributors can try to find appropriate substitutes through googling).


## Git


### Setting up Git

[Quick setting](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git#setting-up-git) up of the `git`

[Git Cheat Sheet](http://training.github.com/downloads/github-git-cheat-sheet/)

To start the development, you'll need to have a code of the repository locally on your machine and have it connected to the remote repository (this GitHub project through `git`), there are three ways to do it (depending on how you've installed and setup your git environment):

1. Using HTTPS URL:
    ```bash
    $ git clone https://github.com/korcky/fairmocracy.git
    ```
2. Using SSH key:
    ```bash
    $ git clone git@github.com:korcky/fairmocracy.git
    ```
3. Usinbg GitHub CLI:
    ```bash
    $ gh repo clone korcky/fairmocracy
    ```


### Contributing workflow

The `main` branch will be protected: the only way to add/change the code is through Pull Requests (PRs).

Step-by-step workflow:

1. Switch to the `main` branch:
    ```bash
    $ git checkout main
    ```
2. Pull latest version of the code in from the `main` branch:
    ```bash
    $ git pull
    ```
    Or optionally specifying the remote and branch:
    ```bash
    $ git pull origin main
    ```
3. Create a new branch locally:
    ```bash
    $ git checkout -b new_branch_name
    ```
    1. The name of the branch should be unique
    2. If you want to be fancy you might follow this naming pattern `<type>[/<task id>]/<short description>`, e.g.:
        1. You're adding a new purple party: `feat/add_purple_party` or `feat/task-2/add_purple_party`
        2. You're fixing a bug with yellow party: `fix/yellow_party_no_votes` or `feat/task-42/yellow_party_no_votes`
4. Make desired changes to the code (e.g. you've created `new_file` and made changes to `old_file`)

5. Add required files to the commit: 
    ```bash
    $ git add new_file old_file
    ```
6. Commit changes:
    ```bash
    $ git commit
    ```
    1. If you want to be fancy you can try to make a short description on what in this commit, e.g. `[fix] yellow party can vote now`
7. Push changes to the remote repository:
    ```bash
    $ git push
    ```
8. Create a PR:
    1. Go to GitHub interface, into `Pull requests` tab
    2. Click on `New pull request`
    3. Choose your branch as a target to be merge into the `main` branch
9. Wait for a review and when it's done click `merge`



## Python

We'll use the latest `Python` version, `3.13.1` as of now.

A general style guide for a nice `Python` code can be found [here](https://peps.python.org/pep-0008/) (I might introduce some automatic formatters for the code later to make your life easier).

I'd recommend to setup a virtual environmet for the `Python` (thing that allows you to separate packages version for different projects). You can do it [the easy way](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments) or, if you'll have more `Python` project in future, my way (whenever your cmd in the repository with `.python-version` file, correct virtual environment will be activatet automatically):

1. Install https://github.com/pyenv/pyenv (not an advanced installation)
2. Install https://github.com/pyenv/pyenv-virtualenv
3. Install the required version of `python` to `pyenv`
    * Run `$ pyenv install 3.13.1`
4. Create a virtual environment based on the installed `python` version (you can choose any name, `fairmocracy` used as an example)
    * Run `$ pyenv virtualenv 3.13.1 fairmocracy`
5. Go to `fairmocracy` directory
6. List all virtual environments: `$ pyenv virtualenvs`
7. In my case there was `3.13.1/envs/fairmocracy (created from ...)`
8. Create `.python-version` with `3.13.1/envs/fairmocracy` in it
    * Run `$ echo "3.13.1/envs/fairmocracy" > .python-version`
9. Run `python --version` to check that it worked (should print `Python 3.13.1`)
