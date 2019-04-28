class Logger:
    def __init__(self):
        self.buffer = ""
    
    def log(self, x):
        self.buffer += f"{x}\n"
    
    def push(self):
        print(self.buffer, end="")
        self.buffer = ""