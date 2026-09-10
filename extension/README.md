# AI Newsletter Collector - Chrome Extension

A simple Chrome extension to collect articles for your weekly AI newsletter with one click.

## Installation

1. **Open Chrome Extensions page:**
   - Go to `chrome://extensions/` in your browser
   - OR: Click the three dots menu → Extensions → Manage Extensions

2. **Enable Developer Mode:**
   - Toggle the "Developer mode" switch in the top-right corner

3. **Load the extension:**
   - Click "Load unpacked"
   - Navigate to: `/Users/agueda.mijachavez/Projects/Newsletter/chrome-extension`
   - Click "Select" or "Open"

4. **Pin the extension (optional but recommended):**
   - Click the puzzle piece icon in your Chrome toolbar
   - Find "AI Newsletter Collector"
   - Click the pin icon to keep it visible

## How to Use

### Saving Articles

**While reading an interesting article:**

1. Click the extension icon in your toolbar
2. Review the article title and URL
3. Choose:
   - **"✓ Save Article"** - Quick save
   - **"📝 Save with Note"** - Add why it's interesting

### Viewing Saved Articles

1. Click the extension icon
2. Click "📋 View Saved Articles"
3. See all your saved articles
4. Delete any you don't want with the "Delete" button

### Exporting to Your Tracker

**When you're ready to generate your newsletter (usually Friday):**

1. Click the extension icon
2. Click "📤 Export for Tracker"
3. Click "📋 Copy to Clipboard"
4. Open `AI Newsletter Tracker.md`
5. Paste into the "Secondary Articles" section
6. Clear the extension's list for next week (delete individual articles)

## Your New Workflow

**Throughout the week:**
1. Reading AI articles → Click extension → Save
2. Extension keeps count (shows "X articles saved")

**Friday:**
1. Click extension → Export → Copy
2. Paste into tracker
3. Run `./prepare.sh`
4. Paste prompt to Claude Code
5. Get newsletter!

## Features

✅ One-click save from any webpage
✅ Optional notes for each article
✅ See count of saved articles
✅ View and manage saved list
✅ Export in perfect format for your tracker
✅ All data stored locally in Chrome (private)

## Tips

- Save articles as you read them (takes 2 seconds)
- Add notes for articles you're excited about
- Review your saved list on Friday before exporting
- Delete any that don't fit the week's theme
- The extension formats everything perfectly for your tracker

## Troubleshooting

**Extension not showing up:**
- Make sure Developer Mode is enabled
- Try reloading the extension page
- Check that you selected the right folder

**Can't click the extension icon:**
- Make sure it's pinned (puzzle piece → pin icon)
- OR click the puzzle piece icon to access it

**Articles not saving:**
- Check that you're on an actual webpage (not chrome:// pages)
- Make sure the page has fully loaded

---

**Need help?** Let Claude Code know and we'll fix it together!
