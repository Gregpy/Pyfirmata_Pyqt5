from pyfirmata import Arduino, util
from time import perf_counter_ns
import matplotlib.pyplot as plt

# Use StandardFirmata (under File -> Examples -> Firmata) on arduino to run this

board = Arduino('COM3') # this may need to be changed
it = util.Iterator(board)
it.start()
analog_input = board.get_pin('a:0:i') # uses input pin A0

times = []
values = [0,0]
clicks = []

time0 = perf_counter_ns() # starting the timer

try:
    
    while 1:
        
        #board.pass_time(0.000001) # use to change loop speed if needed
        
        if analog_input.read() is None: # skip loop when no value is detected
            
            continue

        else:
            
            value = float(analog_input.read()) # should get a numerical value
            values.append(value)
            
            if value > 0.5 and values[-2] < 0.5: # assuming clicks will be greater than 2.5 V and no click will be less than 2.5 V
                
                times.append(perf_counter_ns() - time0)
                clicks.append(1)
                print('Voltage 0-5 V = 0-1:', value, 'ns after start: ', times[-1]) # see live updates of clicks, ns after start
                    
            else:
                
                continue

except KeyboardInterrupt: # ctrl-c to end
    
    board.pass_time(1) # get error if don't pause before exiting
    board.exit()
    plt.plot(times, clicks, 'o')
    plt.xlabel('Time')
    plt.ylabel('Clicks')
    plt.show()
    print('Timestamps: ', times)


except TypeError as error:
    
    print(error)
    board.exit() # best to exit with any errors so board does not have to be replugged in
