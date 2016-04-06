#!/usr/bin/python
import sys, getopt, time, subprocess

def print_stuff():
  print "\nCaptured ctrl+c!"

def exit_clean():
  print_stuff()
  sys.exit(0)

def main():
  loop = True
  seconds = -1
  disk_name = ''
  usage = "Usage:capture_ctr_c_timed_loop.py -t seconds"
  # Read command line args
  try:
    myopts, args = getopt.getopt(sys.argv[1:],"t:")
  except getopt.GetoptError as e:
    #e = sys.exc_info()[0]
    print e
    print usage
    sys.exit()
  ###############################
  # o == option
  # a == argument passed to the o
  ###############################
  for o, a in myopts:
      if o == '-t':
        seconds=int(a)
  #This loop will exit when seconds = 0 or the user presses Crtl + C
  #Either event will trigger the iops_report to be generated
  while loop:
    if seconds == -1:
      print "looping forever! Press CTRL+C to exit..."
    if seconds > 0:
      print "looping for %s seconds..." % ( seconds )
      seconds -= 1
    #If still looping sleep for 1 second
    if loop:
      time.sleep(1)
    if seconds == 0:
      loop = False
    #If still looping sleep for 1 second

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
        exit_clean()
