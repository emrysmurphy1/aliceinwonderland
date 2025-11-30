# Lewis Carroll: A Distant Reading

An interactive web visualization exploring four works by Lewis Carroll through computational text analysis.

**🌐 View Live:** [https://emrysmurphy1.github.io/aliceinwonderland/](https://emrysmurphy1.github.io/aliceinwonderland/)

## About

This project performs distant reading analysis on four Lewis Carroll works:
- **Alice's Adventures in Wonderland**
- **Phantasmagoria and Other Poems**
- **Rhyme? and Reason?**
- **Feeding the Mind**

### Analysis Features

- **Word Frequency Analysis** - Bag of words with stopword filtering
- **Sentiment Analysis** - Polarity (negative to positive) and subjectivity scores
- **Style Metrics** - Sentence length, vocabulary richness, lexical diversity
- **Interactive Word Clouds** - Visual representation of word frequencies
- **Comparative Analysis** - Side-by-side comparison across works

### Design

Victorian/Alice in Wonderland themed interface featuring:
- Vintage color palette (burgundy, forest green, gold)
- Playing card suit decorations (♠ ♥ ♣ ♦)
- Classic serif typography
- Responsive, interactive design

## Project Structure

```
aliceinwonderland/
├── tests/          # Original Lewis Carroll texts from Project Gutenberg
├── analysis/       # Python scripts for text analysis
│   ├── analyze.py      # Main analysis engine
│   ├── preprocess.py   # Text preprocessing utilities
│   └── requirements.txt
└── docs/           # GitHub Pages site
    ├── index.html      # Main web interface
    ├── styles.css      # Victorian theme styling
    ├── app.js          # Interactive visualization logic
    └── data/
        └── analysis.json  # Generated analysis data
```

## Running Locally

### View the Visualization

From the `docs/` directory:
```bash
python3 -m http.server 8000
```
Then open http://localhost:8000 in your browser.

### Re-run the Analysis

To regenerate the analysis data:
```bash
cd analysis
pip install -r requirements.txt
python3 analyze.py
```

This will process the text files and update `docs/data/analysis.json`.

## Technologies

- **Analysis:** Python with NLTK, TextBlob, and NumPy
- **Visualization:** Vanilla JavaScript with Canvas API
- **Styling:** CSS with Victorian aesthetic
- **Deployment:** GitHub Pages

## License

MIT
