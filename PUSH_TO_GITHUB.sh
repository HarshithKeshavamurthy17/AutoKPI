#!/bin/bash

# AutoKPI - Push to GitHub Script
# Replace YOUR_USERNAME with your actual GitHub username

echo "🚀 AutoKPI - Push to GitHub"
echo "================================"
echo ""

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "⚠️  Remote 'origin' already exists!"
    echo "Current remote URL:"
    git remote get-url origin
    echo ""
    read -p "Do you want to update it? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your GitHub username: " GITHUB_USERNAME
        git remote set-url origin "https://github.com/${GITHUB_USERNAME}/AutoKPI.git"
        echo "✅ Remote URL updated!"
    else
        echo "Using existing remote..."
    fi
else
    read -p "Enter your GitHub username: " GITHUB_USERNAME
    git remote add origin "https://github.com/${GITHUB_USERNAME}/AutoKPI.git"
    echo "✅ Remote added!"
fi

echo ""
echo "📤 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🌐 Next step: Deploy on Streamlit Cloud"
    echo "   1. Go to: https://share.streamlit.io"
    echo "   2. Sign in with GitHub"
    echo "   3. Click 'New app'"
    echo "   4. Select: ${GITHUB_USERNAME}/AutoKPI"
    echo "   5. Main file: app.py"
    echo "   6. Click 'Deploy'"
    echo ""
    echo "🎉 Your app will be live at: https://YOUR_APP_NAME.streamlit.app"
else
    echo ""
    echo "❌ Error pushing to GitHub!"
    echo "Make sure you:"
    echo "   1. Created the repository at: https://github.com/new"
    echo "   2. Named it: AutoKPI"
    echo "   3. Have the correct GitHub credentials"
fi



