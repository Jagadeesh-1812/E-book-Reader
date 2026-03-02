import sys
import os
import fitz  # PyMuPDF
import pyttsx3
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                           QComboBox, QSlider, QFileDialog, QMessageBox,
                           QListWidget, QLineEdit, QSplitter, QInputDialog,
                           QDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QIcon, QPalette, QFont, QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
import tempfile


# Image paths
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
LOGO_PATH = os.path.join(IMAGE_DIR, "logo.png")
PLAY_ICON = os.path.join(IMAGE_DIR, "play.png")
PAUSE_ICON = os.path.join(IMAGE_DIR, "pause.png")
HIGHLIGHT_ICON = os.path.join(IMAGE_DIR, "highlight.png")
BOOKMARK_ICON = os.path.join(IMAGE_DIR, "bookmark.png")
NOTE_ICON = os.path.join(IMAGE_DIR, "note.png")
NEXT_ICON = os.path.join(IMAGE_DIR, "next.png")
PREV_ICON = os.path.join(IMAGE_DIR, "prev.png")
ADD_BOOK_ICON = os.path.join(IMAGE_DIR, "add_book.png")

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)
        self.setStyleSheet(APP_STYLE)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo
        if os.path.exists(LOGO_PATH):
            logo_label = QLabel()
            pixmap = QPixmap(LOGO_PATH)
            logo_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(logo_label)
        
        # Title
        title = QLabel("Welcome to E-Book Reader")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 600;
                color: #ffffff;
                margin-bottom: 30px;
            }
        """)
        layout.addWidget(title)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 15px;
                font-size: 16px;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                color: #ffffff;
            }
        """)
        layout.addWidget(self.username_input)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                padding: 15px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        self.login_button.clicked.connect(self.on_login_clicked)
        layout.addWidget(self.login_button)
        
        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #ff4444;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
        
    def on_login_clicked(self):
        username = self.username_input.text().strip()
        if not username:
            self.error_label.setText("Please enter a username")
            return
        self.accept()
        
    def get_username(self):
        return self.username_input.text().strip()
        
    def show_error(self, message):
        self.error_label.setText(message)

# Global styles
APP_STYLE = """
    QMainWindow, QDialog {
        background-color: #121212;
    }
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 12px;
        color: #ffffff;
    }
    QPushButton {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.15);
    }
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 0.2);
    }
    QPushButton:disabled {
        background-color: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.3);
    }
    QTextEdit {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 15px;
        font-size: 14px;
        line-height: 1.6;
        selection-background-color: rgba(255, 255, 255, 0.1);
    }
    QListWidget {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 8px;
    }
    QListWidget::item {
        padding: 12px;
        border-radius: 6px;
        margin: 4px 0;
    }
    QListWidget::item:selected {
        background-color: rgba(255, 255, 255, 0.1);
    }
    QListWidget::item:hover {
        background-color: rgba(255, 255, 255, 0.08);
    }
    QLineEdit {
        padding: 12px;
        border: none;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        font-size: 14px;
    }
    QLineEdit:focus {
        background-color: rgba(255, 255, 255, 0.08);
    }
    QComboBox {
        padding: 12px;
        border: none;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.05);
        color: #ffffff;
        font-size: 14px;
    }
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png);
        width: 12px;
        height: 12px;
    }
    QComboBox QAbstractItemView {
        background-color: rgba(30, 30, 30, 0.95);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 8px;
        selection-background-color: rgba(255, 255, 255, 0.1);
    }
    QSlider::groove:horizontal {
        border: none;
        background: rgba(255, 255, 255, 0.1);
        height: 4px;
        border-radius: 2px;
    }
    QSlider::handle:horizontal {
        background: #ffffff;
        border: none;
        width: 16px;
        margin: -6px 0;
        border-radius: 8px;
    }
    QSlider::handle:horizontal:hover {
        background: rgba(255, 255, 255, 0.9);
    }
    QLabel {
        color: #ffffff;
        font-weight: 500;
        font-size: 14px;
    }
    QSplitter::handle {
        background: rgba(255, 255, 255, 0.1);
        width: 2px;
    }
    QScrollBar:vertical {
        border: none;
        background: rgba(255, 255, 255, 0.05);
        width: 8px;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

class TextToSpeechThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, text, voice_id=None, rate=200):
        super().__init__()
        self.text = text
        self.voice_id = voice_id
        self.rate = rate
        self.is_stopped = False
        self.engine = None
        
    def run(self):
        try:
            self.engine = pyttsx3.init()
            if self.voice_id:
                self.engine.setProperty('voice', self.voice_id)
            self.engine.setProperty('rate', self.rate)
            self.engine.say(self.text)
            self.engine.runAndWait()
            if not self.is_stopped:
                self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit()
    
    def stop(self):
        self.is_stopped = True
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

class EBookReader(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"E-Book Reader - Welcome, {username}")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application style
        self.setStyleSheet(APP_STYLE)
        
        # Initialize variables
        self.current_doc = None
        self.current_page = 0
        self.bookmarks = []
        self.notes = {}
        self.highlights = {}
        self.is_playing = False
        self.tts_thread = None
        
        self.init_ui()
        
    def init_ui(self):
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome message with logo
        welcome_container = QWidget()
        welcome_layout = QHBoxLayout(welcome_container)
        
        if os.path.exists(LOGO_PATH):
            logo_label = QLabel()
            pixmap = QPixmap(LOGO_PATH)
            logo_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
            welcome_layout.addWidget(logo_label)
        
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 600;
                color: #ffffff;
            }
        """)
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addStretch()
        
        main_layout.addWidget(welcome_container)
        
        # Create splitter for left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel (book list and controls)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(15, 15, 15, 15)
        
        # Book list
        self.book_list = QListWidget()
        self.book_list.itemClicked.connect(self.load_book)
        self.book_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(255, 255, 255, 0.05);
                color: #ffffff;
                border: none;
                border-radius: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 6px;
                margin: 4px 0;
            }
            QListWidget::item:selected {
                background-color: rgba(255, 255, 255, 0.1);
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """)
        left_layout.addWidget(QLabel("Your Library"))
        left_layout.addWidget(self.book_list)
        
        # Add book button with icon
        add_book_btn = QPushButton("Add Book")
        if os.path.exists(ADD_BOOK_ICON):
            add_book_btn.setIcon(QIcon(ADD_BOOK_ICON))
            add_book_btn.setIconSize(QSize(24, 24))
        add_book_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        add_book_btn.clicked.connect(self.add_book)
        left_layout.addWidget(add_book_btn)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search in books...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: none;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.05);
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """)
        self.search_box.textChanged.connect(self.search_books)
        left_layout.addWidget(self.search_box)
        
        # TTS controls
        tts_controls = QWidget()
        tts_layout = QVBoxLayout(tts_controls)
        tts_layout.setSpacing(8)
        
        # Voice selection
        self.voice_combo = QComboBox()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            self.voice_combo.addItem(voice.name, voice.id)
        tts_layout.addWidget(QLabel("Voice:"))
        tts_layout.addWidget(self.voice_combo)
        
        # Speed control
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(100)
        self.speed_slider.setMaximum(300)
        self.speed_slider.setValue(200)
        tts_layout.addWidget(QLabel("Speed:"))
        tts_layout.addWidget(self.speed_slider)
        
        left_layout.addWidget(tts_controls)
        
        # Right panel (book content and controls)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        # Book content
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.05);
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 20px;
                font-size: 14px;
                line-height: 1.6;
                selection-background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        right_layout.addWidget(self.text_edit)
        
        # Audio control buttons
        audio_controls = QWidget()
        audio_layout = QHBoxLayout(audio_controls)
        audio_layout.setSpacing(10)
        
        self.play_btn = QPushButton("Play")
        if os.path.exists(PLAY_ICON):
            self.play_btn.setIcon(QIcon(PLAY_ICON))
            self.play_btn.setIconSize(QSize(24, 24))
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        self.play_btn.clicked.connect(self.play_audio)
        audio_layout.addWidget(self.play_btn)
        
        self.pause_btn = QPushButton("Pause")
        if os.path.exists(PAUSE_ICON):
            self.pause_btn.setIcon(QIcon(PAUSE_ICON))
            self.pause_btn.setIconSize(QSize(24, 24))
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        self.pause_btn.clicked.connect(self.pause_audio)
        audio_layout.addWidget(self.pause_btn)
        
        right_layout.addWidget(audio_controls)
        
        # Navigation controls
        nav_controls = QWidget()
        nav_layout = QHBoxLayout(nav_controls)
        nav_layout.setSpacing(10)
        
        prev_btn = QPushButton("Previous")
        if os.path.exists(PREV_ICON):
            prev_btn.setIcon(QIcon(PREV_ICON))
            prev_btn.setIconSize(QSize(24, 24))
        prev_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        prev_btn.clicked.connect(self.prev_page)
        nav_layout.addWidget(prev_btn)
        
        self.page_label = QLabel("Page: 0/0")
        self.page_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        nav_layout.addWidget(self.page_label)
        
        next_btn = QPushButton("Next")
        if os.path.exists(NEXT_ICON):
            next_btn.setIcon(QIcon(NEXT_ICON))
            next_btn.setIconSize(QSize(24, 24))
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        next_btn.clicked.connect(self.next_page)
        nav_layout.addWidget(next_btn)
        
        right_layout.addWidget(nav_controls)
        
        # Action buttons
        action_controls = QWidget()
        action_layout = QHBoxLayout(action_controls)
        action_layout.setSpacing(10)
        
        read_btn = QPushButton("Read Aloud")
        if os.path.exists(PLAY_ICON):
            read_btn.setIcon(QIcon(PLAY_ICON))
            read_btn.setIconSize(QSize(24, 24))
        read_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        read_btn.clicked.connect(self.read_aloud)
        action_layout.addWidget(read_btn)
        
        bookmark_btn = QPushButton("Add Bookmark")
        if os.path.exists(BOOKMARK_ICON):
            bookmark_btn.setIcon(QIcon(BOOKMARK_ICON))
            bookmark_btn.setIconSize(QSize(24, 24))
        bookmark_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        bookmark_btn.clicked.connect(self.add_bookmark)
        action_layout.addWidget(bookmark_btn)
        
        highlight_btn = QPushButton("Highlight")
        if os.path.exists(HIGHLIGHT_ICON):
            highlight_btn.setIcon(QIcon(HIGHLIGHT_ICON))
            highlight_btn.setIconSize(QSize(24, 24))
        highlight_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        highlight_btn.clicked.connect(self.highlight_text)
        action_layout.addWidget(highlight_btn)
        
        note_btn = QPushButton("Add Note")
        if os.path.exists(NOTE_ICON):
            note_btn.setIcon(QIcon(NOTE_ICON))
            note_btn.setIconSize(QSize(24, 24))
        note_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """)
        note_btn.clicked.connect(self.add_note)
        action_layout.addWidget(note_btn)
        
        right_layout.addWidget(action_controls)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
    def add_book(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open E-Book", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.book_list.addItem(os.path.basename(file_path))
            self.load_book(file_path)
            p
    def load_book(self, item):
        if isinstance(item, str):
            file_path = item
        else:
            file_path = item.text()
            
        try:
            self.current_doc = fitz.open(file_path)
            self.current_page = 0
            self.display_page()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {e}")
            
    def display_page(self):
        if self.current_doc:
            page = self.current_doc[self.current_page]
            text = page.get_text()
            self.text_edit.setPlainText(text)
            
            # Reapply highlights for this page
            if self.current_page in self.highlights:
                cursor = self.text_edit.textCursor()
                for highlight in self.highlights[self.current_page]:
                    cursor.setPosition(highlight['start'])
                    cursor.setPosition(highlight['end'], QTextCursor.MoveMode.KeepAnchor)
                    format = QTextCharFormat()
                    format.setBackground(QColor("#FFD700"))
                    format.setForeground(QColor("#000000"))
                    cursor.mergeCharFormat(format)
            
            self.page_label.setText(f"Page: {self.current_page + 1}/{len(self.current_doc)}")
            
    def prev_page(self):
        if self.current_doc and self.current_page > 0:
            self.current_page -= 1
            self.display_page()
            
    def next_page(self):
        if self.current_doc and self.current_page < len(self.current_doc) - 1:
            self.current_page += 1
            self.display_page()
            
    def read_aloud(self):
        if not self.current_doc or self.is_playing:
            return
            
        text = self.text_edit.toPlainText()
        if not text:
            return
            
        voice_id = self.voice_combo.currentData()
        rate = self.speed_slider.value()
        
        # Stop any existing thread
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.stop()
            self.tts_thread.wait()
        
        # Create and start new thread
        self.tts_thread = TextToSpeechThread(text, voice_id, rate)
        self.tts_thread.finished.connect(self.on_tts_finished)
        self.tts_thread.error.connect(self.on_tts_error)
        self.tts_thread.start()
        
        self.is_playing = True
        self.update_play_pause_buttons()
    
    def play_audio(self):
        if not self.is_playing:
            self.read_aloud()
    
    def pause_audio(self):
        if not self.is_playing or not self.tts_thread:
            return
            
        try:
            self.tts_thread.stop()
            self.tts_thread.wait()
            self.is_playing = False
            self.update_play_pause_buttons()
        except Exception as e:
            print(f"Error stopping audio: {e}")
    
    def on_tts_finished(self):
        self.is_playing = False
        self.update_play_pause_buttons()
    
    def on_tts_error(self, error_msg):
        print(f"TTS Error: {error_msg}")
        self.is_playing = False
        self.update_play_pause_buttons()
    
    def update_play_pause_buttons(self):
        self.play_btn.setEnabled(not self.is_playing)
        self.pause_btn.setEnabled(self.is_playing)
        
    def add_bookmark(self):
        if self.current_doc:
            bookmark = {
                'page': self.current_page,
                'title': f"Page {self.current_page + 1}"
            }
            self.bookmarks.append(bookmark)
            QMessageBox.information(self, "Bookmark Added", f"Bookmark added for page {self.current_page + 1}")
            
    def highlight_text(self):
        if not self.current_doc:
            return
            
        cursor = self.text_edit.textCursor()
        if not cursor.hasSelection():
            return
            
        # Get the selected text and its position
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        selected_text = cursor.selectedText()
        
        # Create highlight format
        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor("#FFD700"))
        
        # Apply the highlight
        cursor.mergeCharFormat(highlight_format)
        
        # Store the highlight
        if self.current_page not in self.highlights:
            self.highlights[self.current_page] = []
            
        self.highlights[self.current_page].append({
            'start': start,
            'end': end,
            'text': selected_text
        })
        
        # Update the text edit to show the highlight
        self.text_edit.setTextCursor(cursor)
            
    def add_note(self):
        if self.current_doc:
            text, ok = QInputDialog.getText(self, "Add Note", "Enter your note:")
            if ok and text:
                self.notes[self.current_page] = text
                QMessageBox.information(self, "Note Added", "Note added successfully")
                
    def search_books(self):
        search_text = self.search_box.text().lower()
        for i in range(self.book_list.count()):
            item = self.book_list.item(i)
            if search_text in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
                
    def closeEvent(self, event):
        # Stop any ongoing TTS
        if self.tts_thread and self.tts_thread.isRunning():
            self.tts_thread.stop()
            self.tts_thread.wait()
        
        # Close the document
        if self.current_doc:
            self.current_doc.close()
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Show login window first
    login_window = LoginWindow()
    if login_window.exec() == QDialog.DialogCode.Accepted:
        username = login_window.get_username()
        if username:
            # Show main window with username
            window = EBookReader(username)
            window.show()
            sys.exit(app.exec())
        else:
            QMessageBox.critical(None, "Error", "Please enter a username")
            sys.exit(1)
    else:
        sys.exit(0) 