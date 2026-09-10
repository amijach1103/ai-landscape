// Get current tab information
let currentTab = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    currentTab = tab;

    // Display current page info
    document.getElementById('currentTitle').textContent = tab.title;
    document.getElementById('currentUrl').textContent = tab.url;

    // Load saved articles count
    updateArticleCount();

    // Set up event listeners
    document.getElementById('saveBtn').addEventListener('click', saveCurrentArticle);
    document.getElementById('saveWithNoteBtn').addEventListener('click', showNoteSection);
    document.getElementById('confirmNoteBtn').addEventListener('click', saveWithNote);
    document.getElementById('cancelNoteBtn').addEventListener('click', hideNoteSection);
    document.getElementById('viewBtn').addEventListener('click', toggleSavedList);
    document.getElementById('exportBtn').addEventListener('click', showExport);
    document.getElementById('copyBtn').addEventListener('click', copyToClipboard);
    document.getElementById('copyAndClearBtn').addEventListener('click', copyAndClearAll);
    document.getElementById('closeExportBtn').addEventListener('click', closeExport);
});

// Save current article without note
async function saveCurrentArticle() {
    await saveArticle(currentTab.title, currentTab.url, null);
}

// Show note input section
function showNoteSection() {
    document.getElementById('noteSection').classList.remove('hidden');
    document.getElementById('noteInput').focus();
}

// Hide note input section
function hideNoteSection() {
    document.getElementById('noteSection').classList.add('hidden');
    document.getElementById('noteInput').value = '';
}

// Save article with note
async function saveWithNote() {
    const note = document.getElementById('noteInput').value.trim();
    await saveArticle(currentTab.title, currentTab.url, note || null);
    hideNoteSection();
}

// Save article to storage
async function saveArticle(title, url, note) {
    try {
        // Get existing articles
        const result = await chrome.storage.local.get(['articles']);
        const articles = result.articles || [];

        // Check if already saved
        if (articles.some(a => a.url === url)) {
            showFeedback('Article already saved!', 'error');
            return;
        }

        // Add new article
        articles.push({
            title,
            url,
            note,
            savedAt: new Date().toISOString()
        });

        // Save back to storage
        await chrome.storage.local.set({ articles });

        // Update UI
        updateArticleCount();
        showFeedback('✓ Article saved!', 'success');

    } catch (error) {
        showFeedback('Error saving article', 'error');
        console.error(error);
    }
}

// Update article count display
async function updateArticleCount() {
    const result = await chrome.storage.local.get(['articles']);
    const articles = result.articles || [];
    document.getElementById('articleCount').textContent = articles.length;

    // Count articles from this week (last 7 days)
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const weekCount = articles.filter(article => {
        if (!article.savedAt) return false;
        return new Date(article.savedAt) >= oneWeekAgo;
    }).length;

    document.getElementById('weekCount').textContent = weekCount;
}

// Toggle saved articles list
async function toggleSavedList() {
    const listElement = document.getElementById('savedList');

    if (!listElement.classList.contains('hidden')) {
        listElement.classList.add('hidden');
        return;
    }

    const result = await chrome.storage.local.get(['articles']);
    const articles = result.articles || [];

    if (articles.length === 0) {
        listElement.innerHTML = '<div class="empty-state">No articles saved yet</div>';
    } else {
        listElement.innerHTML = articles
            .sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt))
            .map((article, index) => `
                <div class="saved-item">
                    <div class="saved-item-title">${escapeHtml(article.title)}</div>
                    <div class="saved-item-url">${escapeHtml(article.url)}</div>
                    ${article.note ? `<div class="saved-item-note">${escapeHtml(article.note)}</div>` : ''}
                    <button class="delete-btn" data-url="${escapeHtml(article.url)}">Delete</button>
                </div>
            `).join('');

        // Add delete handlers
        listElement.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', () => deleteArticle(btn.dataset.url));
        });
    }

    listElement.classList.remove('hidden');
}

// Delete article
async function deleteArticle(url) {
    const result = await chrome.storage.local.get(['articles']);
    const articles = result.articles || [];
    const filtered = articles.filter(a => a.url !== url);

    await chrome.storage.local.set({ articles: filtered });
    updateArticleCount();
    toggleSavedList(); // Refresh the list
    showFeedback('Article removed', 'success');
}

// Show export view
async function showExport() {
    const result = await chrome.storage.local.get(['articles']);
    const articles = result.articles || [];

    if (articles.length === 0) {
        showFeedback('No articles to export', 'error');
        return;
    }

    // Format for tracker
    const formatted = articles
        .sort((a, b) => new Date(b.savedAt) - new Date(a.savedAt))
        .map(article => {
            const date = new Date(article.savedAt);
            const dateStr = date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                year: 'numeric'
            });
            let line = `* [${article.title}](${article.url}) | ${dateStr}`;
            if (article.note) {
                line += ` (${article.note})`;
            }
            return line;
        })
        .join('\n');

    document.getElementById('exportText').value = formatted;
    document.getElementById('exportOutput').classList.remove('hidden');
    document.getElementById('savedList').classList.add('hidden');
}

// Copy to clipboard
async function copyToClipboard() {
    const text = document.getElementById('exportText').value;

    try {
        await navigator.clipboard.writeText(text);
        showFeedback('✓ Copied to clipboard!', 'success');
    } catch (error) {
        // Fallback method
        document.getElementById('exportText').select();
        document.execCommand('copy');
        showFeedback('✓ Copied to clipboard!', 'success');
    }
}

// Copy to clipboard and clear all articles
async function copyAndClearAll() {
    const text = document.getElementById('exportText').value;

    try {
        await navigator.clipboard.writeText(text);

        // Clear all articles
        await chrome.storage.local.set({ articles: [] });

        // Update UI
        updateArticleCount();
        closeExport();
        showFeedback('✓ Copied & cleared! Fresh start.', 'success');
    } catch (error) {
        // Fallback method
        document.getElementById('exportText').select();
        document.execCommand('copy');

        await chrome.storage.local.set({ articles: [] });
        updateArticleCount();
        closeExport();
        showFeedback('✓ Copied & cleared! Fresh start.', 'success');
    }
}

// Close export view
function closeExport() {
    document.getElementById('exportOutput').classList.add('hidden');
}

// Show feedback message
function showFeedback(message, type) {
    const feedback = document.getElementById('feedback');
    feedback.textContent = message;
    feedback.className = `feedback ${type}`;
    feedback.classList.remove('hidden');

    setTimeout(() => {
        feedback.classList.add('hidden');
    }, 3000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
