

class EventBus():
    def __init__(self):
        self.Functions = {}
        self.Variables = {}

    def SetFunction(self, nameFunction: str, function: callable = None):
        if nameFunction not in self.Functions:
            self.Functions[nameFunction] = []
        if function not in self.Functions[nameFunction] and function is not None:
            self.Functions[nameFunction].append(function)

    def SetVariable(self, nameVariable: str, value):
        self.Variables[nameVariable] = value

    def GetFunction(self, nameFunction: str,*attr,**kwargs):
        if nameFunction in self.Functions:
            for function in self.Functions[nameFunction]:
                function(*attr,**kwargs)

    def GetVariable(self, nameVariable: str):
        return self.Variables.get(nameVariable)