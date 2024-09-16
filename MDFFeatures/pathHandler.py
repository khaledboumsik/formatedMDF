class PathHandler:
    def __init__(self, InputPath=None, OutputPath=None) -> None:
        self._input_path = InputPath
        self._output_path = OutputPath

    @property
    def InputPath(self):
        return self._input_path

    @InputPath.setter
    def InputPath(self, value):
        self._input_path = value

    @property
    def OutputPath(self):
        return self._output_path

    @OutputPath.setter
    def OutputPath(self, value):
        self._output_path = value