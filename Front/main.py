import os
import sys

sys.path[0]=sys.path[0]+"\\.."
print(sys.path[0])
import subprocess
from threading import Thread
from PyQt5.QtWidgets import (
     QMainWindow,QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
    QListWidget, QLabel, QAbstractItemView
)
from Front.Healpers.CSVLoader import process_csv_files
from MDFFeatures.CSVConverter import CSVConverter
from MDFFeatures.pathHandler import PathHandler
import mdfreader
from MDFFeatures.fileHandler import FileHandler

class FileSelectorApp(QMainWindow):
    """this is the main file it is responsable for the launch on the application and the program should be packaged from this file 
    """
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_processing = False

    def initUI(self):
        """
        this is the entier gui application with all the functions directly linked"""
        self.setWindowTitle('File Selector App')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.buttonLayout = QHBoxLayout()

        # Input directory selection button
        self.inputDirButton = QPushButton('Select Input Directory')
        self.inputDirButton.clicked.connect(self.selectInputDirectory)
        self.buttonLayout.addWidget(self.inputDirButton)

        # Output directory selection button
        self.outputDirButton = QPushButton('Select Output Directory')
        self.outputDirButton.clicked.connect(self.selectOutputDirectory)
        self.buttonLayout.addWidget(self.outputDirButton)

        # Open button
        self.openButton = QPushButton('Open')
        self.openButton.clicked.connect(self.processSelectedFiles)
        self.buttonLayout.addWidget(self.openButton)

        # Transform button
        self.transformButton = QPushButton('Transform')
        self.transformButton.clicked.connect(self.transformFiles)
        self.buttonLayout.addWidget(self.transformButton)

        # Generate Report button
        self.generateReportButton = QPushButton('Generate Report')
        self.generateReportButton.clicked.connect(self.generateReport)
        self.buttonLayout.addWidget(self.generateReportButton)

        self.layout.addLayout(self.buttonLayout)

        self.fileListLayout = QHBoxLayout()

        # File list widgets
        self.availableFilesListWidget = QListWidget()
        self.availableFilesListWidget.setAcceptDrops(True)
        self.fileListLayout.addWidget(self.availableFilesListWidget)

        self.arrowLayout = QVBoxLayout()
        self.leftToRightButton = QPushButton('→')
        self.leftToRightButton.clicked.connect(self.transferToSelected)
        self.arrowLayout.addWidget(self.leftToRightButton)

        self.rightToLeftButton = QPushButton('←')
        self.rightToLeftButton.clicked.connect(self.transferToAvailable)
        self.arrowLayout.addWidget(self.rightToLeftButton)

        self.fileListLayout.addLayout(self.arrowLayout)

        self.selectedFilesListWidget = QListWidget()
        self.selectedFilesListWidget.setAcceptDrops(True)
        self.selectedFilesListWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.fileListLayout.addWidget(self.selectedFilesListWidget)

        self.layout.addLayout(self.fileListLayout)

        self.selectedFileLabel = QLabel('Selected file information will be shown here.')
        self.layout.addWidget(self.selectedFileLabel)

        self.inputDirectory = ''
        self.outputDirectory = ''

    def selectInputDirectory(self):
        """this is used to prompt the user to select an input directory
        """
        directory = QFileDialog.getExistingDirectory(self, 'Select Input Directory')
        if directory:
            self.inputDirectory = directory
            self.updateFileList()

    def selectOutputDirectory(self):
        """this is used to prompt the user to select an output directory
        """
        directory = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        if directory:
            self.outputDirectory = directory
            self.updateFileList()

    def updateFileList(self):
        """this is used to update the values inside the available side (left)
        """
        if self.outputDirectory:
            self.availableFilesListWidget.clear()
            for file_name in os.listdir(self.outputDirectory):
                file_path = os.path.join(self.outputDirectory, file_name)
                if os.path.isfile(file_path):
                    self.availableFilesListWidget.addItem(file_name)

    def transferToSelected(self):
        """this is used to move items from the leftside (available) to the right side (selected)
        """
        selected_items = self.availableFilesListWidget.selectedItems()
        if selected_items:
            selected_files = [self.selectedFilesListWidget.item(i).text() for i in range(self.selectedFilesListWidget.count())]
            for item in selected_items:
                self.selectedFilesListWidget.addItem(item.text())
                self.availableFilesListWidget.takeItem(self.availableFilesListWidget.row(item))
                selected_files.append(item.text())

    def transferToAvailable(self):
        """this is used to move items from the right side (selected) to the leftside (available)
        """
        selected_items = self.selectedFilesListWidget.selectedItems()
        for item in selected_items:
            self.availableFilesListWidget.addItem(item.text())
            self.selectedFilesListWidget.takeItem(self.selectedFilesListWidget.row(item))

    def processSelectedFiles(self):
        """once the files are selected this will take in all the iteams highlighted and runs the table
        script on them to show case the generated file
        """
        selected_items = self.selectedFilesListWidget.selectedItems()
        if selected_items:
            if not self.current_processing:
                self.current_processing = True
                for item in selected_items:
                    file_name = item.text()
                    file_path = os.path.join(self.outputDirectory, file_name)
                    if not file_name.lower().endswith('.csv'):
                        self.selectedFileLabel.setText("Selected file is not a CSV.")
                        self.current_processing = False
                        return
                    self.run_command(file_path)
                self.current_processing = False
            else:
                self.selectedFileLabel.setText("A file is already being processed.")

    def transformFiles(self):
        """this function calls upon the files stored in the MDFFeatures those files are responsable for 
        creating the csv that is required for the process to function it will soon have pandas support and
        cache features#TODO
        """
        if not self.inputDirectory or not self.outputDirectory:
            self.selectedFileLabel.setText("Both input and output directories must be selected.")
            return
        
        pathhandler1 = PathHandler(self.inputDirectory, self.outputDirectory)
        converter1 = CSVConverter(mdfreader, self.outputDirectory)
        fileh = FileHandler(pathhandler1, converter1)
        fileh.convert()

        selected_items = self.selectedFilesListWidget.selectedItems()
        if selected_items:
            if not self.current_processing:
                self.current_processing = True
                for item in selected_items:
                    file_name = item.text()
                    input_file_path = os.path.join(self.inputDirectory, file_name)
                    output_file_path = os.path.join(self.outputDirectory, file_name.replace('.mdf', '.csv'))

                    if not file_name.lower().endswith('.mdf'):
                        self.selectedFileLabel.setText("Selected file is not an MDF.")
                        self.current_processing = False
                        return

                    self.run_command(input_file_path, output_file_path)
                self.current_processing = False
                
            else:
                self.selectedFileLabel.setText("A file is already being processed.")
        self.updateFileList()
    def generateReport(self):
        print("try")
        """this function uses the Selected files to generate a report 
        this report contains the file name and how many distinct occurences of a certain Default code
        
        """
        if not self.outputDirectory:
            self.selectedFileLabel.setText("Output directory must be selected.")
            return

        selected_items = self.selectedFilesListWidget.selectedItems()
        if selected_items:
            if not self.current_processing:
                self.current_processing = True
                
                # Collect the file paths of the selected files
                file_paths = [os.path.join(self.outputDirectory, item.text()) for item in selected_items]
                
                # Call the process_csv_files function with the list of file paths
                process_csv_files(file_paths)
                
                # Path to the generated report file
                report_file_path = os.path.join(self.outputDirectory, 'combined_output.csv')
                
                # Run the tabler.py script on the generated report file
                if os.path.exists(report_file_path):
                    try:

                        command = ['python',  '.\\front\\SubWidgets\\table.py', report_file_path]
                        print(command)
                        # Execute the command
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        stdout, stderr = process.communicate()
                        
                        # Check the process output
                        if process.returncode == 0:
                            self.selectedFileLabel.setText(f"Report generated and tabler.py executed successfully:\n{stdout}")
                        else:
                            self.selectedFileLabel.setText(f"tabler.py execution failed with error:\n{stderr}")
                    
                    except Exception as e:
                        self.selectedFileLabel.setText(f"An error occurred while running tabler.py: {e}")
                else:
                    self.selectedFileLabel.setText("Generated report file not found.")
                
                self.current_processing = False
            else:
                self.selectedFileLabel.setText("A file is already being processed.")

    def run_command(self, file_path):
        """this funtion is responsable for calling the table by bash command thus utilises multi threading to 
        open multiple tables at once and let's the use manipulates them

        Args:
            file_path (str): this is the path of the file you want to display it is currently in csv format
            but will soon implement a no intermidiate format via pandas #TODO
        """
        def target():
            try:
                command = ['python', '.\\front\\SubWidgets\\table.py', file_path]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    self.selectedFileLabel.setText(f"Command output:\n{stdout}")
                else:
                    self.selectedFileLabel.setText(f"Command failed with error:\n{stderr}")
            
            except Exception as e:
                self.selectedFileLabel.setText(f"An error occurred: {e}")

        thread = Thread(target=target)
        thread.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileSelectorApp()
    window.show()
    sys.exit(app.exec_())
