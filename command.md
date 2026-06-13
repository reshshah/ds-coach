

1. Open the folder in VSCode
bashcode /Users/rshah/Claude

2. Initialize Git and connect to your GitHub repo
Open the terminal inside VSCode (Ctrl+`) and run:
cd /Users/rshah/Claude

# Initialize git if not already done
git init

# Connect to your existing GitHub repo
git remote add origin https://github.com/reshshah/ds-coach.git

# Verify the connection
git remote -v

3. Create your .gitignore
In the same terminal:

touch .gitignore
open .gitignore

Add the specific files and folders you want to exclude. Example:
# Ignore specific markdown files
career.md
current_focus.md
command.md

# Ignore specific folders
/Engg Blogs Webinar/
/Reel Transcriber/

# Common ignores
.DS_Store
.env
__pycache__/
*.pyc

Replace the file and folder names with your actual ones. Tell me what they are and I can write the exact .gitignore for you.

4. Push to GitHub
git add .
git commit -m "initial commit"
git branch -M main
git push -u origin main
If you get an auth error on push, you need a GitHub Personal Access Token. Let me know and I will walk you through that.

5. Claude Code setup (optional but recommended)
If you want Claude Code to be aware of your project context, add a CLAUDE.md file at the root:

touch CLAUDE.md

Then add CLAUDE.md to .gitignore if you do not want it pushed:
CLAUDE.md
