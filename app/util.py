import os
import git
import time
from git import Repo
from config import repo_folder, repo_url
from subprocess import run
from app import scheduler


def clone_repo(url, dest_folder):
    """Cloning github repository function
    
    Deletes the repo folder if exists
    
    Cloning the repo from url
    
    """    
    try:
        if os.path.exists(dest_folder):
            # Remove folder
            run(["rm", "-rf", dest_folder])
        
        Repo.clone_from(url, dest_folder)
    except Exception as e:
        print(f"Error cloning repository: {e}")
        
        
def check_and_clone():
    """Repo check function
    
    checks if repo exists localy - if not clone the repo
    
    fetches the latest changes
    
    check current and remote head commits
    
    if they are not the same, updating by cloning the repo
    """
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
                clone_repo(repo_url, repo_folder)
            else:
                print("No new changes detected.")
        except Exception as e:
            print(f"Error checking repository: {e}")
    else:
        print(f"Repository not found locally. Cloning the repo...")
        clone_repo()
        
        
@scheduler.task('cron', day_of_week='mon', hour=4)
def weekly_task():
    """scheduler task
    
    runs the check and clone function for cloning the repo every monday at 4 AM
    
    """
    check_and_clone()
    print("Weekly task... Check if security standards had been updated.")