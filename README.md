# E-Book Reader with Text-to-Speech

A Python-based E-Book Reader application that supports PDF files and includes text-to-speech functionality.

## Features

- Read PDF e-books
- Text-to-speech conversion with multiple language support
- Adjustable speech speed and voice selection
- Text highlighting
- Bookmarking pages
- Adding notes to text
- Search functionality
- Book organization

## Requirements

- Python 3.8 or higher
- Required packages (install using `pip install -r requirements.txt`):
  - PyQt6
  - PyMuPDF
  - gTTS
  - playsound

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python ebook_reader.py
   ```

2. Add books:
   - Click the "Add Book" button to import PDF files
   - Your books will appear in the library list on the left

3. Reading features:
   - Use the navigation buttons to move between pages
   - Click "Read Aloud" to have the text read to you
   - Adjust voice and speed settings in the left panel
   - Highlight text by selecting it and clicking "Highlight"
   - Add bookmarks using the "Add Bookmark" button
   - Add notes to selected text using the "Add Note" button
   - Search through your library using the search box

## Notes

- The application currently supports PDF files only
- Text-to-speech requires an internet connection
- Bookmarks and notes are stored in memory and will be lost when the application is closed 
