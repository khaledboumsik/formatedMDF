import os
import pickle
from asammdf import MDF

class PandasConverter():
    def __init__(self,OutputPath) -> None:
        self.cached=set(os.listdir(OutputPath))
    def convert(self, input_path, output_path):
        file_name = os.path.basename(input_path).replace('.mdf', '')  # Adjust based on your file extension
        pickled_file_path = os.path.join(self.OutputPath, file_name + ".pkl")

        if file_name + ".pkl" in self.cached:
            print(f"The file with the name {file_name} is already converted.")
            with open(pickled_file_path, 'rb') as file:
                data = pickle.load(file)
            return data
        else:
            print(f"Processing file: {input_path}")
            print(f"Output path: {output_path}")
            mdf_obj = MDF(input_path)
            df = mdf_obj.to_dataframe()
            
            with open(pickled_file_path, 'wb') as file:
                pickle.dump(df, file)
            
            self.cached.add(file_name)