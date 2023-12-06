import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QDialog, QLabel, QHBoxLayout
from PyQt6.QtGui import QPalette, QColor
import PyPDF2
class PDFCombinerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.pdf_files = []

        self.init_ui()

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Add Files Button
        add_files_btn = QPushButton('Add Files', self)
        add_files_btn.clicked.connect(self.add_files)
        layout.addWidget(add_files_btn)

        # List Widget to display added files
        self.file_list_widget = QListWidget(self)
        layout.addWidget(self.file_list_widget)

        # Combine Button
        combine_btn = QPushButton('Combine PDFs', self)
        combine_btn.clicked.connect(self.combine_pdfs)
        layout.addWidget(combine_btn)

        # Set the layout
        self.setLayout(layout)

        #change colors
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        self.setPalette(palette)

    def add_files(self):
        # Open a file dialog to select PDF files
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter('PDF files (*.pdf)')

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            self.pdf_files.extend(selected_files)

            # Update the list widget with added files
            self.file_list_widget.addItems([file for file in selected_files])

    def combine_pdfs(self):
        if not self.pdf_files:
            print('No PDF files added.')
            return
        # Create a PdfWriter
        pdf_writer = PyPDF2.PdfWriter()

        # Loop through all the PDF files.
        for pdf_file in self.pdf_files:
            pdf_file_obj = open(pdf_file, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)

            # Loop through all the pages (except the first) and add them.
            for page_num in range(len(pdf_reader.pages)):
                page_obj = pdf_reader.pages[page_num]
                pdf_writer.add_page(page_obj)

        # Save the resulting PDF to a file.
        output_path, _ = QFileDialog.getSaveFileName(self, 'Save Combined PDF', filter='PDF files (*.pdf)')
        if output_path:
            pdf_output = open(output_path, 'wb')
            pdf_writer.write(pdf_output)
            pdf_output.close()

            # Display a message box
            self.show_completion_message()
    def show_completion_message(self):
        # Create a custom dialog
        dialog = CustomDialog(self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # Clear the list and allow the user to add new files
            self.pdf_files.clear()
            self.file_list_widget.clear()
        elif result == QDialog.DialogCode.Rejected:
            # Exit the application
            self.close()

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Combine PDFs')
        self.setMinimumWidth(300)

        # Layout
        layout = QVBoxLayout()

        # Information Label
        info_label = QLabel('PDFs combined successfully.')
        layout.addWidget(info_label)

        # Buttons
        button_layout = QHBoxLayout()

        combine_new_btn = QPushButton('Combine New', self)
        combine_new_btn.clicked.connect(self.accept)
        button_layout.addWidget(combine_new_btn)

        exit_btn = QPushButton('Exit', self)
        exit_btn.clicked.connect(self.reject)
        button_layout.addWidget(exit_btn)

        layout.addLayout(button_layout)

        # Set the layout
        self.setLayout(layout)

        #change dialog box color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255,255,255))
        self.setPalette(palette)

if __name__ == '__main__':
    app = QApplication([])
    window = PDFCombinerApp()
    window.show()
    app.exec()