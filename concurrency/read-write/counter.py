import threading
class Counter():

    def __init__(self, count):
        assert count > 0
        self.count = count

    def __iter__(self):
        return self
    
    def next(self):
        if self.count == 0:
            raise StopIteration
        self.count -= 1
        return self.count

class ThreadCounter:

    def __init__(self, value):
        assert value > 0
        self.value = value
        self.lock = threading.Lock()

    def __iter__(self):
        return self
        
    def next(self):
        with self.lock:
            if self.value == 0:
                raise StopIteration 
            self.value -= 1 
            return self.value
    
def test_count(klass, count):
    print ("Testing '%s' with count %d" % (klass.__name__, count))
    c = klass(count)
    for i in c:
        print i
        if c == 1:
            break

if __name__ == '__main__':

    test_count(Counter, 5)
    test_count(ThreadCounter, 5)
    
