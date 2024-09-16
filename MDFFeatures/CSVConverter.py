from MDFFeatures.standardConverter import StandardConverter
import os
class CSVConverter(StandardConverter):
    def __init__(self,MDFReader,OutputPath) -> None:
        super().__init__(MDFReader)
        self.cached=set(os.listdir(OutputPath))
    def convert(self, input_path, output_path):
        file_name = os.path.basename(input_path)
        
        if file_name in self.cached:
            print("File already converted.")
            print("Press 'Y' if you would like to reconvert, or any other key to ignore.")
            command = input().strip()
            
            if command.upper() != "Y":
                print("Ignoring file.")
                return

        # Perform the conversion
        print(f"Processing file: {input_path}")
        print(f"Output path: {output_path}")
        
        # Assuming self.MDFReader.Mdf is defined elsewhere
        yop = self.MDFReader.Mdf(input_path)
        output_file = os.path.join(output_path, file_name.replace(".mdf", ".csv"))
        yop.export_to_csv(file_name=output_file)
        
        # Update the cache
        self.cached.add(file_name)
        print(f"File converted and saved to: {output_file}")