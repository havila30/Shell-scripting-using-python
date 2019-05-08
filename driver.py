import os
import sys
from virtual_memory import *

def kvargs(sysargs):
    args = {}

    for val in sysargs[1:]:
        k, v = val.split('=')
        args[k] = v
    return args

def read_file(file_path, delimiter = " "):
    if not os.path.isfile(file_path):
        print("Error: file does not exist in function 'read_file'...")
        return None
    with open(file_path) as f:
        data = f.read()
    data = data.strip()
    return data.split(delimiter)

if __name__ == "__main__":
    args = kvargs(sys.argv)
    if 'directory' in args:
        # print("directory: " + args['directory'])
        pass
    else:
        print("Error: 'directory' should be on command line...")
        sys.exit()

    file_list = os.listdir(args['directory'])
    for file in file_list:
        file_path = os.path.join(args['directory'], file)
        # read the file
        input_data = read_file(file_path)

        # get the simulation information
        file_name = os.path.basename(file_path)             # get basename
        name, ext = file_name.split('.')                    # split name from extension
        sim, run, np, vm_size, pm_size = name.split('_')    # get each piece of info
        vm_size = int(vm_size)
        pm_size = int(pm_size)
        page_size = int(pm_size / 2)

        #########
        print("Simulating file {}".format(file_name))
        print("PM size = {}  VM size = {} count of process = {}".format(pm_size, vm_size, np))

        # print the result

        algo_list = ["FIFO", "LRU", "LFU", "Random"];
        for algo in algo_list:
            # create a virtual memory
            vm = virtual_memory(vm_size, pm_size, page_size, algo)

            # simulate
            statistics = vm.simulate(input_data)
            for process in sorted(statistics.keys()):
                fault_count = statistics[process]
                print("{:>8} PROCESS {:8} {:8}"
                      .format(algo, process, fault_count))


