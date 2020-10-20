import subprocess
import shutil
import argparse
import atexit
import os

parser = argparse.ArgumentParser(description="Installs node_modules into a directory and runs ng serve.")
parser.add_argument('top', metavar='TopDirectory', type=str, help='The top level directory to wherever the homework is located.')
parser.add_argument('ng', metavar='ngDirectory', type=str, help='The Angular directory for a particular homework.')
args = parser.parse_args();

def main():
  atexit.register(move_node_modules_at_exit);

  move_and_install_node_modules();

  run_ng_serve();


# Moves the node_modules folder back to the grading folder for future use
def move_node_modules_at_exit():
  source_path = args.top + "/" + args.ng + "/node_modules";

  if os.path.isdir(source_path):
    print("Moving node_modules back to grading folder.");

    destination_path = "node_modules";

    shutil.move(source_path, destination_path);
    print("Finished moving node_modules.");


# Moves and installs node modules
def move_and_install_node_modules():
  # check if node files exist
  # move them to angular directory if they do
  if os.path.isdir("node_modules"):
    print("Copying node_modules to Angular directory. Do not close this program.");

    destination_path = args.top + "/" + args.ng + "/node_modules";

    shutil.move("node_modules", destination_path);
    print("Finished copying node_modules to Angular directory.\n");

  # run npm install
  npm_install_location = "./" + args.top + "/" + args.ng;
  subprocess.run(["npm", "install"], shell=True, cwd=npm_install_location);


# Runs ng serve at the location specified by the arguments
def run_ng_serve():
  # run ng serve after npm install is done
  ng_serve_location = "./" + args.top + "/" + args.ng;
  pid = subprocess.Popen(["ng", "serve", "<", "nul"], shell=True, cwd=ng_serve_location);

  with pid as p:
    try:
      p.wait()
    except:
      p.kill()
      p.wait()
      # raise

  


if __name__ == "__main__": 
  main();