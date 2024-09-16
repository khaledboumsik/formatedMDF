from MDFFeatures.pathHandler import PathHandler
import os
from MDFFeatures.standardConverter import StandardConverter
class FileHandler:

    def __init__(self,Paths=PathHandler(),Converter=StandardConverter()) -> None:
        self.Paths=Paths
        self.Converter=Converter
        self.Files=[]
        self.counter=0
        self.extractMDFs()
        pass
    def extractMDFs(self):
        for file in os.listdir(self.Paths.InputPath):
            print("file",file)
            if file.upper().endswith(".MDF"):
                self.Files.append({"id":self.counter,"filePath":file})
                self.counter+=1
    def convert(self):
        for filePath in self.Files:
            self.Converter.convert(os.path.join(self.Paths.InputPath,filePath['filePath']),self.Paths.OutputPath)

    