# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. **Go to GitHub**: Open https://github.com/new in your browser

2. **Create new repository**:
   - Repository name: `wing-audio-converter`
   - Description: `Cross-platform audio converter for Behringer Wing multi-channel recordings`
   - Choose: Public (so GitHub Actions work for free) or Private (if you prefer)
   - **DO NOT** check "Add a README file"
   - **DO NOT** add .gitignore or license
   - Click "Create repository"

## Step 2: Push Your Code

After creating the repository, GitHub will show you some commands. **Ignore those** and run these instead:

```bash
cd /Users/macstudio/Applications/wing-audio-converter

# Add your GitHub repository (replace YOUR-USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/wing-audio-converter.git

# Push your code
git branch -M main
git push -u origin main
```

**Example**: If your GitHub username is "johnsmith", the command would be:
```bash
git remote add origin https://github.com/johnsmith/wing-audio-converter.git
```

## Step 3: Watch the Build

1. After pushing, go to your repository on GitHub
2. Click the **"Actions"** tab at the top
3. You'll see a workflow running called "Build Wing Converter for All Platforms"
4. Click on it to watch the progress
5. It will build:
   - ✅ Windows executable (.exe)
   - ✅ macOS app bundle (.app)
   - ✅ Linux executable

The build takes about 5-10 minutes.

## Step 4: Download the Windows Build

Once the build completes (green checkmark):

1. Click on the completed workflow run
2. Scroll down to "Artifacts" section
3. Download **"wing-converter-windows"**
4. Unzip the downloaded file
5. Inside you'll find `Wing Converter Pro.exe`

You can now share this `.exe` file with Windows users! They just double-click it to run - no Python or FFmpeg installation needed.

## Troubleshooting

**"Permission denied" when pushing**:
- GitHub may ask you to authenticate
- Use a Personal Access Token instead of password
- Go to: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token with "repo" scope
- Use the token as your password when prompted

**Build fails**:
- Check the Actions tab and click on the failed job to see error details
- Common issues are usually with FFmpeg download - just re-run the workflow

## What Happens Next?

Every time you push code to GitHub, it will automatically rebuild the executables for all platforms. This means:
- You make changes on your Mac
- Push to GitHub
- GitHub builds Windows/macOS/Linux versions automatically
- Download and distribute the new versions

This is completely free for public repositories!

---

## Ready to Push?

Copy your GitHub username and run:
```bash
git remote add origin https://github.com/YOUR-USERNAME/wing-audio-converter.git
git push -u origin main
```

Then check the Actions tab to watch your build!
