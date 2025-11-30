// Lewis Carroll Distant Reader - Interactive Visualization
let analysisData = null;
let currentBook = null;
let selectedBooks = new Set();

// Initialize the application
async function init() {
    try {
        // Load analysis data
        const response = await fetch('data/analysis.json');
        analysisData = await response.json();

        // Setup UI
        renderBookNavigation();
        setupEventListeners();

        // Select first book by default
        if (analysisData.books.length > 0) {
            selectBook(analysisData.books[0].id);
        }
    } catch (error) {
        console.error('Error loading analysis data:', error);
        document.querySelector('.content').innerHTML =
            '<p style="color: red;">Error loading analysis data. Please ensure the analysis has been run.</p>';
    }
}

// Render book navigation buttons
function renderBookNavigation() {
    const nav = document.getElementById('bookNav');
    nav.innerHTML = analysisData.books.map(book => `
        <button class="book-btn" data-book-id="${book.id}">
            ${book.short_title}
        </button>
    `).join('');
}

// Setup event listeners
function setupEventListeners() {
    // Book navigation
    document.getElementById('bookNav').addEventListener('click', (e) => {
        if (e.target.classList.contains('book-btn')) {
            selectBook(e.target.dataset.bookId);
        }
    });

    // View switching
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchView(e.target.dataset.view);
        });
    });

    // Comparison checkboxes
    document.querySelectorAll('.compare-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateComparison);
    });
}

// Select a book
function selectBook(bookId) {
    const book = analysisData.books.find(b => b.id === bookId);
    if (!book) return;

    currentBook = book;

    // Update active state
    document.querySelectorAll('.book-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.bookId === bookId);
    });

    // Update views
    renderOverview(book);
    renderWordCloud(book);
}

// Switch between views
function switchView(viewName) {
    // Update active view button
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === viewName);
    });

    // Show selected view
    document.querySelectorAll('.view').forEach(view => {
        view.classList.toggle('active', view.id === `${viewName}-view`);
    });
}

// Render overview for a book
function renderOverview(book) {
    // Update title
    document.getElementById('current-title').textContent = book.title;

    // Render metrics
    const metricsGrid = document.getElementById('metricsGrid');
    metricsGrid.innerHTML = `
        <div class="metric-card">
            <div class="metric-label">Total Words</div>
            <div class="metric-value">${book.style.total_words.toLocaleString()}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Unique Words</div>
            <div class="metric-value">${book.style.unique_words.toLocaleString()}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Sentences</div>
            <div class="metric-value">${book.style.total_sentences.toLocaleString()}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Sentence Length</div>
            <div class="metric-value">${book.style.avg_sentence_length}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Word Length</div>
            <div class="metric-value">${book.style.avg_word_length}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Vocabulary Richness</div>
            <div class="metric-value">${book.style.vocabulary_richness}%</div>
        </div>
    `;

    // Render sentiment
    const sentimentDisplay = document.getElementById('sentimentDisplay');
    const polarityPercent = ((book.sentiment.polarity + 1) / 2 * 100).toFixed(1);
    const subjectivityPercent = (book.sentiment.subjectivity * 100).toFixed(1);

    sentimentDisplay.innerHTML = `
        <div class="sentiment-bar">
            <div class="sentiment-label">Polarity (Negative ← → Positive)</div>
            <div class="bar-container">
                <div class="bar-fill polarity" style="width: ${polarityPercent}%">
                    ${book.sentiment.polarity.toFixed(3)}
                </div>
            </div>
        </div>
        <div class="sentiment-bar">
            <div class="sentiment-label">Subjectivity (Objective ← → Subjective)</div>
            <div class="bar-container">
                <div class="bar-fill subjectivity" style="width: ${subjectivityPercent}%">
                    ${book.sentiment.subjectivity.toFixed(3)}
                </div>
            </div>
        </div>
    `;

    // Render top words
    const topWords = document.getElementById('topWords');
    const topWordsArray = Object.entries(book.word_frequencies)
        .slice(0, 30)
        .map(([word, count]) => `
            <div class="word-tag">
                <div class="word-text">${word}</div>
                <div class="word-count">${count}</div>
            </div>
        `).join('');
    topWords.innerHTML = topWordsArray;
}

// Render word cloud on canvas
function renderWordCloud(book) {
    const canvas = document.getElementById('wordCloudCanvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size
    canvas.width = 900;
    canvas.height = 600;

    // Clear canvas
    ctx.fillStyle = '#ede4d3';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Get word frequencies
    const words = Object.entries(book.word_frequencies).slice(0, 50);
    const maxFreq = Math.max(...words.map(([_, count]) => count));

    // Colors from our theme
    const colors = ['#6b2737', '#2d5016', '#d4af37', '#c41e3a', '#1c1c1c'];

    // Place words
    const positions = [];
    words.forEach(([word, count], index) => {
        // Calculate font size based on frequency
        const fontSize = Math.max(14, (count / maxFreq) * 80);
        ctx.font = `${fontSize}px Garamond, Georgia, serif`;

        // Random color from theme
        ctx.fillStyle = colors[Math.floor(Math.random() * colors.length)];

        // Try to place word
        let placed = false;
        let attempts = 0;
        const maxAttempts = 50;

        while (!placed && attempts < maxAttempts) {
            // Spiral placement
            const angle = attempts * 0.5;
            const radius = attempts * 8;
            const x = canvas.width / 2 + Math.cos(angle) * radius;
            const y = canvas.height / 2 + Math.sin(angle) * radius;

            const metrics = ctx.measureText(word);
            const width = metrics.width;
            const height = fontSize;

            // Check bounds
            if (x - width/2 > 0 && x + width/2 < canvas.width &&
                y - height/2 > 0 && y + height/2 < canvas.height) {

                // Check overlap with existing words
                let overlaps = false;
                for (const pos of positions) {
                    if (!(x + width/2 < pos.x - pos.width/2 ||
                          x - width/2 > pos.x + pos.width/2 ||
                          y + height/2 < pos.y - pos.height/2 ||
                          y - height/2 > pos.y + pos.height/2)) {
                        overlaps = true;
                        break;
                    }
                }

                if (!overlaps) {
                    ctx.fillText(word, x - width/2, y);
                    positions.push({ x, y, width, height });
                    placed = true;
                }
            }

            attempts++;
        }
    });
}

// Update comparison view
function updateComparison() {
    selectedBooks.clear();
    document.querySelectorAll('.compare-checkbox:checked').forEach(cb => {
        selectedBooks.add(cb.value);
    });

    if (selectedBooks.size === 0) {
        document.getElementById('comparisonDisplay').innerHTML =
            '<p style="text-align: center; color: #6b2737; font-size: 1.2em;">Select books to compare</p>';
        return;
    }

    const booksToCompare = analysisData.books.filter(b => selectedBooks.has(b.id));

    // Create comparison table
    let html = '<div class="comparison-table"><h3>Style Metrics Comparison</h3><table>';
    html += '<tr><th>Metric</th>';
    booksToCompare.forEach(book => {
        html += `<th>${book.short_title}</th>`;
    });
    html += '</tr>';

    const metrics = [
        { key: 'total_words', label: 'Total Words', format: v => v.toLocaleString() },
        { key: 'unique_words', label: 'Unique Words', format: v => v.toLocaleString() },
        { key: 'total_sentences', label: 'Sentences', format: v => v.toLocaleString() },
        { key: 'avg_sentence_length', label: 'Avg Sentence Length', format: v => v },
        { key: 'avg_word_length', label: 'Avg Word Length', format: v => v },
        { key: 'vocabulary_richness', label: 'Vocabulary Richness %', format: v => v }
    ];

    metrics.forEach(metric => {
        html += `<tr><td><strong>${metric.label}</strong></td>`;
        booksToCompare.forEach(book => {
            html += `<td>${metric.format(book.style[metric.key])}</td>`;
        });
        html += '</tr>';
    });

    html += '</table></div>';

    // Add sentiment comparison
    html += '<div class="comparison-table"><h3>Sentiment Comparison</h3><table>';
    html += '<tr><th>Book</th><th>Polarity</th><th>Subjectivity</th></tr>';
    booksToCompare.forEach(book => {
        html += `<tr>
            <td><strong>${book.short_title}</strong></td>
            <td>${book.sentiment.polarity.toFixed(3)}</td>
            <td>${book.sentiment.subjectivity.toFixed(3)}</td>
        </tr>`;
    });
    html += '</table></div>';

    document.getElementById('comparisonDisplay').innerHTML = html;
}

// Start the application
init();
