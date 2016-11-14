import smbus

class SMBusInterface:

    def __init__(self, dummyMode):
        self.dummyMode = dummyMode
        if(self.dummyMode is False):
            self.smbus = smbus.SMBus(1)
            self.address = 0x04
    
    def writeByte(self, byte):
        if(self.dummyMode is False):
            self.smbus.write_byte(self.address, byte)
        
    def motorOpen(self, isMouth):
        value = 0x85 if isMouth else 0x05
        self.writeByte(value)
        
    def motorClose(self, isMouth):
        value = 0x86 if isMouth else 0x06
        self.writeByte(value)

    def motorHold(self, isMouth):
        value = 0x87 if isMouth else 0x07
        self.writeByte(value)

    def motorMoveToState(self, state, isMouth):
        value = 0x80 if isMouth else 0x00
        value = (value | state) 
        self.writeByte(value)

