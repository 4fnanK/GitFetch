import os
import subprocess
import requests
import sys
from tqdm import tqdm 

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"User '{username}' not found.")
        sys.exit(1)
    else:
        print(f"Failed to fetch repositories. Status code: {response.status_code}")
        sys.exit(1)

def clone_repos(repos, username):
    if not repos:
        print("No repositories found.")
        return

    # Create a directory for the user's repositories
    base_dir = os.path.join(os.getcwd(), username)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    print(f"\nFound {len(repos)} repositories. Cloning into folder: '{base_dir}'...\n")
    
    for repo in tqdm(repos, desc="Cloning repositories", unit="repo"):
        repo_name = repo["name"]
        clone_url = repo["clone_url"]
        repo_dir = os.path.join(base_dir, repo_name)
        
        # Check if the repo already exists in the folder
        if not os.path.exists(repo_dir):
            subprocess.run(["git", "clone", clone_url, repo_dir])
        else:
            print(f"Repository '{repo_name}' already exists. Skipping...")

def main():
    print("\n 𝙶𝚒𝚝𝙵𝚎𝚝𝚌𝚑𝚎𝚛, GɪᴛHᴜʙ Rᴇᴘᴏsɪᴛᴏʀʏ Cʟᴏɴᴇʀ")
    print("Clone All Repositories of a GitHub User \n")
    print("_________________________________________\n")
    
    username = input("Enter the GitHub username: ").strip()
    
    if not username:
        print("Username cannot be empty.")
        sys.exit(1)

    print(f"\nFetching repositories for user '{username}'...\n")
    repos = fetch_repos(username)
    
    clone_repos(repos, username)
    
    print(f"\nAll repositories have been cloned into the '{username}' folder successfully!")

if __name__ == "__main__":
    main()
