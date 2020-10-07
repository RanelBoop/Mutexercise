import pickle
import threading
import time

class Db:
    def _loader(self,name):
        try :
            with open(name,"rb") as file:
                self.dict = pickle.load(file)
            #file closes automatically after with open() block
        except FileNotFoundError:
            file = open(name,"w+")
            file.close()
            #doesnt automatically close
        except EOFError:
            pass

    def __init__(self,name):
        self.name = name
        self.dict = {}
        self._loader(name)

    def _read(self,key):
        self._loader(self.name)
        value = self.dict.get(key, "empty")
        return value
        #print("read: {} : {} ".format(key,value))

    def _write(self,key,value):
        self.dict[key] = value
        with open(self.name,"wb") as file:
            pickle.dump(self.dict, file)
        print("wrote: {} = {} ".format(key,value))
        #print("whole database: " + str(self.dict))

class SecDb(Db):
    def __init__(self,name,):
        super().__init__(name)
        self.semaphore = threading.Semaphore(10)
        self.writeLock = threading.Lock() #RLock
        self.readLock = threading.Lock()
        self.readerCount = 0
        self.viewLock = threading.Lock()

    def _read(self,key):
        '''
        self.semaphore.acquire()
        self.mutex.acquire()
        self.mutex.release()
        super()._read(key)
        print("Reading...")
        #time.sleep(0.5)
        self.semaphore.release()
        '''


        '''
        def _write(self,key,value):
        super()._write(key,value)
        print("Writing...")
        time.sleep(1)
        '''


            #except threading.ThreadError:
                #print("content is currently occupied...")

    def write(self, Range):
        self.writeLock.acquire()
        self.viewLock.acquire()
        try:
            print("writing...")
            for x in range(Range):
                super()._write(x,x*2)
                time.sleep(1)
        finally:
            print("finished Writing!")
            self.viewLock.release()
            self.writeLock.release()


    def read(self, key):
        self.viewLock.acquire()
        self.viewLock.release()

        self.semaphore.acquire()


        self.readLock.acquire()
        self.readerCount += 1
        if self.readerCount == 1 : self.writeLock.acquire()
        self.readLock.release()
        try:
            value = super()._read(key)
            print("No.{} reading...".format(key))
            time.sleep(5)
        finally:
            print("Reader No.{} Got: {}".format(key, value))
            self.semaphore.release()
            self.readLock.acquire()
            self.readerCount -= 1
            self.readLock.release()
            if self.readerCount == 0: self.writeLock.release()








database = SecDb("Dictionary.txt")

def main():
    #Read and write without concurrency

    print("Basic Test: ")
    database._write("john","oliver")
    database._read("john")

def main2():
    #Write vs Write
    writer1 = threading.Thread(target = database.write,args =(3,))
    writer1.start()
    print("starting second writer")
    writer2 = threading.Thread(target = database.write,args = (3,))
    writer2.start()



def main3():
    #Readers vs Writer

    threads = []
    print("creating one writer")
    writer = threading.Thread(target = database.write,args = (15,))
    writer.start()
    print("starting readers")
    for y in range(15):
        reader = threading.Thread(target = database.read,args = (y,))
        reader.start()
        threads.append(reader)
    time.sleep(16)
    print("starts writing")
    writer =threading.Thread(target = database.write,args = (7,))
    writer.start()




if __name__ == "__main__":
    main3()

