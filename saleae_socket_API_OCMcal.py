import saleae
import os
import argparse

def capture_formatter(number):
    
    number_str = "000"
    
    if number < 10:
        number_str = "00{}".format(number)
    elif number < 100:
        number_str = "0{}".format(number)
    elif number < 1000:
        number_str = "{}".format(number)
    else:
        number_str = "To large a number"

    return number_str

parser = argparse.ArgumentParser(description='Saleae Command Line Interface Capture Utility')
parser.add_argument('-cc', '--capture-count', required=True, type=int, metavar='COUNT', help='number of captures to repeat')
parser.add_argument('-cd', '--capture-duration', required=True, type=float, metavar='SECONDS', help='duration of each capture in seconds')
#parser.add_argument('-sc', '--save-captures', metavar='PATH', help='if specified, saves each capture to the specified directory')
#parser.add_argument('-ed', '--export-data', metavar='PATH', help='if specified, exports the raw capture to the sepcified directory')
parser.add_argument('-ea', '--export-analyzers', metavar='PATH', help='if specified, exports each analyzer to the specified directory')
parser.add_argument('-tn', '--test-name', metavar='NAME', default="Shitname", help='Test name will be the first of the filename')
parser.add_argument('-ip', '--ip_addr', metavar='IP', default='localhost', help='optional, IP address to connect to. Default localhost')
parser.add_argument('-port', '--port', metavar='PORT', default=10429, help='optional, Port to connect to. Default 10429')

args = parser.parse_args()

# Connect to saleae logic software on extern ip
s = saleae.Saleae(args.ip_addr, args.port)

#set capture duration
s.set_capture_seconds(args.capture_duration)

total_capture = capture_formatter(args.capture_count)

for x in range(args.capture_count):
    
    #Start the capture
    s._cmd('CAPTURE')
    
    #analyzer export
    if args.export_analyzers != None:
        analyzers = s.get_analyzers()
        if analyzers.count == 0:
            print("Now analyzer pressent in the Logic software")
        for analyzer in analyzers:
            file_name = "{0}_OPC{1}_{2}OF{3}.txt".format(args.test_name, analyzer[1], capture_formatter(x+1), total_capture)
            save_path = os.path.join(args.export_analyzers, file_name)
            print(save_path)
            s.export_analyzer(analyzer[1], save_path)
        