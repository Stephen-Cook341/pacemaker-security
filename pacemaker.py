

class Pacemaker():
    
    def __init__(self,pacemaker_id,pacemaker_addr):
        
        self.pacemaker_id = pacemaker_id
        self.pacemaker_addr = pacemaker_addr
        
    def get_pacemaker_id(self):
        return self.pacemaker_id
    
    def get_pacemaker_addr(self):
        return self.pacemaker_addr
        