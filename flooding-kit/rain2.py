import time
import botbook_mcp3002 as mcp #

rainLevel= 0

def readRainLevel():
        global rainLevel
        rainLevel= mcp.readAnalog(0, 1 ) # the second param is which port of MCP3002 you want to read(eg: want to read CH0 set it is 0, want to read output from CH1 set 1)

def main():
        while True: #
                readRainLevel() #
                print ("Current rain level is %i " % rainLevel) #
                time.sleep(0.5) # s

if __name__=="__main__":
        main()
