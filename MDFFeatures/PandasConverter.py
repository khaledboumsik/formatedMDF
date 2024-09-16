from MDFFeatures.standardConverter import StandardConverter
import os
import pickle
class CSVConverter(StandardConverter):
    def __init__(self,MDFReader,OutputPath) -> None:
        self.OutputPath=OutputPath
        super().__init__(MDFReader)
        self.cached=set(os.listdir(OutputPath))
    def convert(self, input_path, output_path):
        file_name = os.path.basename(input_path)
        
        if file_name in self.cached:
            print(f"The file with the name {file_name} is already converted.")
            with open(os.path.join(input_path,file_name+".pkl"), 'rb') as file:
                data = pickle.load(file)
            return data
        else:
            # Perform the conversion
            print(f"Processing file: {input_path}")
            print(f"Output path: {output_path}")
            
            # Assuming self.MDFReader.Mdf is defined elsewhere
            yop = self.MDFReader.Mdf(input_path)
            yop.convert_to_pandas()
            yop.to_pickle(os.path.join(self.OutputPath,file_name+".pkl"))
            # Update the cache
            self.cached.add(file_name)
        return yop