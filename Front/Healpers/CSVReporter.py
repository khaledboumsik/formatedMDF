from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd
class CSVLoaderThread(QThread):
    finished = pyqtSignal(pd.DataFrame, str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            chunksize = 10000
            df = pd.read_csv(self.file_path, chunksize=chunksize)
            df_combined = pd.concat(df)
            self.finished.emit(df_combined, self.file_path)
        except Exception as e:
            self.finished.emit(None, str(e))
