

class resultFromController():
    def __init__(self, isSuccess, Message):
        self.isSuccess = isSuccess
        self.Message =Message

    def __str__(self):
        return "isSuccess "+str(self.isSuccess)+ " msg: "+ self.Message