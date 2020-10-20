import subprocess
import signal
import sys
import argparse


parser = argparse.ArgumentParser(description="Runs Angular and node.js environments for a specified directory")
parser.add_argument('top', metavar='TopDirectory', type=str, help='The top level directory to wherever the homework is located.')
parser.add_argument('ng', metavar='ngDirectory', type=str, help='The Angular directory for a particular homework.')
parser.add_argument('node', metavar='nodeDirectory', type=str, help='The Node.JS directory for a particular homework.')
args = parser.parse_args();

pid = None;

def signal_handler(signum, frame):
  global pid;
  global nodePid
  if pid:
    pid.kill();
    nodePid.kill();
    print("\nEnding Processes", flush=True);
    pid = None;
    nodePid = None;
  else:
    sys.exit(1);

signal.signal(signal.SIGINT, signal_handler);

#pid = subprocess.call(["python3", "child.py"], shell=True);

pid = subprocess.Popen(["python3", "ng.py", args.top, args.ng])

nodePid = subprocess.Popen(["python3", "node.py", args.top, args.node])
            
pid.wait();