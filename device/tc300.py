from serial import Serial
  
class TC300() :
    def __init__(self, logger=None ) :
        """  Initialize dome properties and capabilities
        """
        print('init')
        self.maxswitch = 1
        self.description = 'Thorlabs TC 300'
        self.name = 'Iodine temperature'
        self.minswitchvalue = 0
        self.maxswitchvalue = 80
        self.connect(port='COM7')

    def connect(self,port='COM7') :
        print('connect')
        self.tc300=Serial(port,115200,timeout=1)
        self.connected = True

    def connected(self,state) :
        print('connected',state)
        return state

    def canwrite(self,id) :
        return True

    def disconnect(self) :
        self.connected(False)

    def get_description(self,id) :
        return self.description

    def get_name(self,id) :
        return self.name

    def get_minvalue(self,id) :
        return self.minswitchvalue

    def get_maxvalue(self,id) :
        return self.maxswitchvalue

    def set_value(self,id,val) :
        print('setting value',val)
        self.tc300.write(b'TSET{:d}={:s}\r'.format(id,val).encode())
        self.tc300.readline()
        self.tc300.write(b'EN{:d}=1\r'.format(id,val).encode())
        self.tc300.readline()

    def getswitch(self,id) :
        return True

    def get_value(self,id) :
        print('getting value')
        self.tc300.write(b'TSET{:d}?\r'.format(id).encode())
        return self.tc300.readline()

    def get_volt(self,id) :
        print('getting value')
        self.tc300.write(b'VOLT{:d}?\r'.format(id).encode())
        return self.tc300.readline()

    def get_current(self,id) :
        print('getting value')
        self.tc300.write(b'CURR{:d}?\r'.format(id).encode())
        return self.tc300.readline()

    def get_step(self,id) :
         return 0.1

