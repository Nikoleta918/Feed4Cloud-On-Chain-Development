import time
import multiprocessing
import RTFS

class Scheduler(multiprocessing.Process):
  daemon = True

  def __init__(self):
    multiprocessing.Process.__init__(self)
    self.stop_event = multiprocessing.Event()

  def stop(self):
    self.stop_event.set()

  def run(self):
    try:
      while (True):
        RTFS.RTFS()
        time.sleep(10)
    except Exception as exception:
      print("Read error")


if __name__ == '__main__':
  print("Starting Scheduler")

  scheduler = Scheduler()
  try:
    scheduler.run()
  except KeyboardInterrupt:
    print("Keyboard Interrupt detected")
    scheduler.stop()
