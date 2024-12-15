import os
import git
from git import Repo
from config import repo_folder, repo_url
from subprocess import run

def clone_repo():
    try:
        if os.path.exists(repo_folder):
            # Remove folder
            run(["rm", "-rf", repo_folder])
        
        Repo.clone_from(repo_url, repo_folder)
    except Exception as e:
        print(f"Error cloning repository: {e}")
        
        
def check_and_clone():
    # Check if the directory already exists
    if os.path.isdir(repo_folder):
        try:
            # Open the existing repository
            repo = Repo(repo_folder)
            # Fetch the latest changes
            origin = repo.remotes.origin
            origin.fetch()
            
            # Check the current and remote HEAD commits
            local_commit = repo.head.commit.hexsha
            remote_commit = origin.refs.main.commit.hexsha

            if local_commit != remote_commit:
                print(f"Changes detected! Cloning the repo...")
                clone_repo()
            else:
                print("No new changes detected.")
        except Exception as e:
            print(f"Error checking repository: {e}")
    else:
        print(f"Repository not found locally. Cloning the repo...")
        clone_repo()