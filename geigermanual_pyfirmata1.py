from pyfirmata import Arduino, util
from time import perf_counter_ns

# Use StandardFirmata (under File -> Examples -> Firmata) on arduino to run this

board = Arduino('COM3') # this may need to be changed
it = util.Iterator(board)
it.start()
analog_input = board.get_pin('a:0:i') # uses input pin A0

times = []
values = [0,0]
clicks = []
numCount = 0
maxCount = 10
time0 = perf_counter_ns() # starting the timer

print(board)
print(analog_input)
print('Max count:', maxCount)
print('Press ctrl-c to end early and print timestamps')

try:
    
    while 1:

        #board.pass_time(0.000001) # use to change loop speed if needed, seconds
        
        if analog_input.read() is None: # skip loop if None value is detected
            
            continue

        else:
            
            value = float(analog_input.read())*5 # should get a numerical value, 0-1 = 0-5 V
            values.append(value)
            
            if value > 1.5 and values[-2] < 1.5: # assuming clicks will be greater than 1.5 V and no click will be less than 1.5 V
                
                times.append(perf_counter_ns() - time0)
                clicks.append(1)
                print('Voltage V:', value, 'ns after start: ', times[-1]) # see live updates of clicks, ns after start
                    
            else:
                
                continue
        
        numCount += 1
        
        if numCount == maxCount:
            
            board.pass_time(1) # pause before exiting or get error
            board.exit()
            print('Timestamps: ', times)
            break
        
except KeyboardInterrupt: # ctrl-c to end
    
    board.pass_time(1)
    board.exit()
    print('Timestamps: ', times)

except TypeError as error:
    
    print(error)
    board.pass_time(1)
    board.exit() # best to exit with any errors so board does not have to be replugged in
