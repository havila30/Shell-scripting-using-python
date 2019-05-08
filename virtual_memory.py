import random
import sys

g_time_counter = 0

class page_frame(object):
    def __init__(self, page_number):
        self.page_number = page_number  # virtual page number

        self.valid_bit = False              # in memory
        self.dirty = False                  # updated
        self.last_access = 0                # time stamp

        self.access_history = []            # time stamp history

    def access(self):
        global g_time_counter

        self.last_access = g_time_counter
        self.access_history.append(g_time_counter)

class physical_memory(object):
    def __init__(self, mem_size, page_size, replacement_algorithm):
        self.mem_size = int(mem_size)
        self.page_size = int(page_size)
        self.max_page_count = int(self.mem_size / self.page_size)
        self.replacement_algorithm = replacement_algorithm

        self.mem_table = {}         # dictionary of page_frames

    def _selectPageByFIFO(self, page):
        key = list(self.mem_table.keys())[0]
      
        return key

    def _selectPageByLRU(self, page):
        key = list(self.mem_table.keys())[0]
        value = self.mem_table[key].last_access

        for i in self.mem_table:
            if (value < self.mem_table[i].last_access):
                key = i
                value = self.mem_table[i].last_access

        return key

    def _selectPageByRandom(self, page):
        key_list = list(self.mem_table.keys())
        index = random.randint(0, len(key_list) - 1)
        key = key_list[index]

        return key

    def _selectPageByLFU(self, page):
        global g_time_counter

        t0 = g_time_counter - 20
        if t0 < 0:
            t0 = 0

        # calculate the access count since t0 per each page frame
        min = sys.maxsize
        key = None
        for i in self.mem_table:
            access_count = 0
            for t in reversed(self.mem_table[i].access_history):
                if t < t0:
                    break
                access_count += 1
            if min > access_count:
                min = access_count
                key = i

        return key

    def _selectPageByOptimal(self, page):
        pass

    def _replacePage(self, page):
        if self.replacement_algorithm == "FIFO":
            key = self._selectPageByFIFO(page)
        elif self.replacement_algorithm == "LRU":
            key = self._selectPageByLRU(page)
        elif self.replacement_algorithm == "LFU":
            key = self._selectPageByLFU(page)
        elif self.replacement_algorithm == "Random":
            key = self._selectPageByRandom(page)
        elif self.replacement_algorithm == "Optimal":
            key = self._selectPageByOptimal(page)
            
        # print("Swap out page: {}".format(self.mem_table[key].page_number))

        del self.mem_table[key]
        self.mem_table[page.page_number] = page

    def _getEmptyPage(self):
        for i in range(self.max_page_count):
            if i not in self.mem_table:
                return i

    def checkPageExistence(self, page):
        if page.page_number in self.mem_table:
            return True
        else:
            return False
    def insertPage(self, page):
        if len(self.mem_table) >= self.max_page_count:
            self._replacePage(page)
        else:
            self.mem_table[page.page_number] = page

class page_table(object):
    def __init__(self, virt_mem_size, phys_mem_obj, page_size):
        self.vm_size = virt_mem_size
        self.phys_mem_obj = phys_mem_obj
        self.page_size = page_size

        self.page_table = {}        # dictionary of page_frames
        self.fault_count = 0

    def accessPage(self, page_number):
        page = {}
        if page_number not in self.page_table:                  # no page_frame in the page_table
            self.fault_count += 1  # mark as a fault
            page = self.page_table[page_number] = page_frame(page_number)  # create a new page_frame
            self.phys_mem_obj.insertPage(page)                  # insert the page into physical memory
            # print("Insert into page_table: {}".format(page.page_number))
        else:
            page = self.page_table[page_number]
            if not self.phys_mem_obj.checkPageExistence(page):  # not exist in physical memory
                self.fault_count += 1                           # mark as a fault
                self.phys_mem_obj.insertPage(page)              # insert the page into physical memory
                # print("Insert into physical memory: {}".format(page.page_number))
            else:
                # print("Found page in physical memory: {}".format(page.page_number))
                pass

        # update the access information
        page.access()

    def getFaultCount(self):
        return self.fault_count

class virtual_memory(object):
    def __init__(self, virt_mem_size, phys_mem_size, page_size, replacement_algorithm):
        self.virt_mem_size = virt_mem_size
        self.phys_mem_size = phys_mem_size
        self.page_size = page_size
        self.replacement_algorithm = replacement_algorithm

        self.page_tables = {}
        self.phys_mem_obj = None

        self.timer_counter = 0

    def traceInstruction(self, process, address):
        global g_time_counter

        if process not in self.page_tables:
            self.page_tables[process] = page_table(self.virt_mem_size, self.phys_mem_obj, self.page_size)

        page_number = int(address / self.page_size)
        # page_offset = int(address) % self.page_size

        self.page_tables[process].accessPage(page_number)
        g_time_counter += 1

    def simulate(self, input_data):
        # initialize the page tables
        self.page_tables = {}

        # initialize the physical memory
        self.phys_mem_obj = physical_memory(self.phys_mem_size, self.page_size, self.replacement_algorithm)

        # trace the instructions
        for item in input_data:
            process, hex_address = item.split(',')
            process = int(process)
            address = int(hex_address, 16)
            self.traceInstruction(process, address)

        # return the statistics
        statistics = {}
        for idx, item in self.page_tables.items():
            statistics[idx] = item.getFaultCount()
        return statistics

if __name__ == "__main__":
    pass
