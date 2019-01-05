import os 
class sensor(object):
    def __init__(self, name):
        self.name = name
        self.count=0
        self.AlarmCount=0


    def graph(self,i):

        self.curve = i.plot.plot(self.time, self.data, pen=self.pen, symbolBrush=self.symb, symbolSize=10,symbolPen='w',symbol=self.symbols,name=self.name)
        #symbol=self.symbol,symbolName=self.name

        i.plot.setLabel('bottom', 'Time', 's')
        #self.plot.setRange( yRange=[0, 6])
    def alarm(self,occurance,data):
        
        print("this is " + str(data))
        if (data<=0.36 and self.AlarmCount <= occurance):
           os.system("mpv rtdsound/" + self.name + ".mp3")
           self.AlarmCount+=1
        else:
          pass

    def update(self,data1,t):
        self.data[:-1] = self.data[1:]
        self.data[-1] = data1

        self.curve.setData(x=self.time,y=self.data)
        self.curve.setPos(t, 0)

    #file handling
    def text(self):
        ph = open("phone.txt", "r")

        self.PhoneNumbers = []
        for line in ph:
            self.PhoneNumbers.append(line)
        ph.close()


    def write(self,ard,k):


        if(k==1):
            self.file.write(ard + " Time")
            self.file.write("\n")
        elif(k==-1):
            self.file.write(ard)
            self.file.write("\n")
        else:
            self.file.write(ard + " ")

    def start(self):
        self.file = open(self.fName, "w+")
    def close(self):
        self.file.close()


    def chk(self,rtd,const):

       if (rtd<const):

          message = self.name + "has problem please go to lab"

          if (self.count == 0):
             for i, line in enumerate(self.PhoneNumbers):
                 send("Warning", line, message)

          self.count += 1
          if (self.count == 25):
                self.count = 0
