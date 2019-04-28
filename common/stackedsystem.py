
class StackedSystem:
    """
    Allows multiple high-level components to call a single low-level component

    Each component that wants to call a StackedSystem must feed() it
    The most 'dominant' (recent) component to call will be the one to have its data execute() ed.
    """
    data = ()

    def feed(self, *kwargs):
        self.data = kwargs
    
    def execute(self):
        print("Tried to call un-overriden StackedSystem with data:")
        print(self.data)