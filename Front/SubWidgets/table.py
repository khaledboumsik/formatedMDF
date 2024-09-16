import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from difflib import get_close_matches
import pickle
class PandasModel(QAbstractTableModel):
    def __init__(self, data_frame, parent=None):
        super(PandasModel, self).__init__(parent)
        self._data_frame = data_frame

    def rowCount(self, parent=QModelIndex()):
        return len(self._data_frame)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data_frame.columns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data_frame.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data_frame.columns[section]
            else:
                return str(section)
        return None

    def get_column_index(self, column_name):
        """ Return the index of the column closest to column_name """
        columns = self._data_frame.columns.tolist()
        closest_match = get_close_matches(column_name, columns, n=1, cutoff=0.6)
        if closest_match:
            return columns.index(closest_match[0])
        return -1

class CSVViewer(QMainWindow):
    def __init__(self, data_frames_with_titles):
        super().__init__()

        self.setWindowTitle("CSV Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        layout = QVBoxLayout()

        # Search box and button
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter column name...")
        search_button = QPushButton("Find Column")
        search_button.clicked.connect(self.search_column)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Store the table views
        self.table_views = []
        layout.addWidget(QLabel(data_frames_with_titles[0]))
        table_view = QTableView()
        model = PandasModel(data_frames_with_titles[1])
        table_view.setModel(model)
        self.table_views.append((data_frames_with_titles[0], table_view, model))
        layout.addWidget(table_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def search_column(self):
        column_name = self.search_input.text()
        if not column_name:
            return

        found = False
        for title, table_view, model in self.table_views:
            col_index = model.get_column_index(column_name)
            if col_index != -1:
                # Scroll to the column
                table_view.horizontalScrollBar().setValue(col_index * table_view.columnWidth(0))
                table_view.setCurrentIndex(model.index(0, col_index))
                found = True
                break

        if not found:
            print(f"Column '{column_name}' not found.")

def concatenate_csv_files(file_paths):
    df_list = []
    titles = []
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)
            df['Source File'] = file_path  # Add a column indicating the source file
            df_list.append(df)
            titles.append(f"Contents of {file_path.split('\\')[-1]}")  # Create a title for each file
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
    
    # Combine the DataFrames and titles
    data_frames_with_titles = list(zip(titles, df_list))
    return data_frames_with_titles


def ProcessPickledDF(file_path):
    with open(file_path, 'rb') as file:
        # Deserialize the data from the file
        df = pickle.load(file)
    df['Source File'] = file_path  # Add a column indicating the source file
    title=f"Contents of {file_path.split('/')[-1]}"  # Create a title for each file
    data_frames_with_titles = [title, df] 
    return data_frames_with_titles

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tabler.py <path_to_csv_file1> <path_to_csv_file2> ...")
        sys.exit(1)

    file_paths = sys.argv[1:]
    data_frames_with_titles = ProcessPickledDF(file_paths[0])
    app = QApplication(sys.argv)
    viewer = CSVViewer(data_frames_with_titles)
    viewer.show()
    sys.exit(app.exec_())
