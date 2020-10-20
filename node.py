import subprocess
import shutil
import argparse
import atexit
import os

parser = argparse.ArgumentParser(description="Installs node_modules into a directory and runs node app.js.")
parser.add_argument('top', metavar='TopDirectory', type=str, help='The top level directory to wherever the homework is located.')
parser.add_argument('node', metavar='nodeDirectory', type=str, help='The node directory for a particular homework.')
args = parser.parse_args();

def main():
  atexit.register(move_node_modules_at_exit);

  move_and_install_node_modules();

  run_node_appjs();


# Moves the node_modules folder back to the grading folder for future use
def move_node_modules_at_exit():
  # Rename file to node_modules_node before moving
  source_path = args.top + "/" + args.node + "/node_modules";
  os.rename(source_path, "node_modules_node");

  source_path += "_node";

  if os.path.isdir(source_path):
    print("Moving node_modules back to grading folder.");

    destination_path = "node_modules_node";

    shutil.move(source_path, destination_path);
    print("Finished moving node_modules.");


# Moves and installs node modules
def move_and_install_node_modules():
  # check if node files exist
  # move them to node directory if they do
  if os.path.isdir("node_modules_node"):
    print("Copying node_modules to Node directory. Do not close this program.");

    destination_path = args.top + "/" + args.node + "/node_modules_node";

    shutil.move("node_modules_node", destination_path);
  
    # Rename file to node_modules
    rename = args.top + "/" + args.node + "/node_modules";
    os.rename(destination_path, rename);

    print("Finished copying node_modules to Node directory.\n");

  # run npm install
  npm_install_location = "./" + args.top + "/" + args.node;
  subprocess.run(["npm", "install"], shell=True, cwd=npm_install_location);


# Runs node app.js at the location specified by the arguments
def run_node_appjs():
  # run node app.js after npm install is done
  node_serve_location = "./" + args.top + "/" + args.node;
  pid = subprocess.Popen(["node", "app.js", "<", "nul"], cwd=node_serve_location);
  
  with pid as p:
    try:
      p.wait()
    except:
      p.kill()
      p.wait()
      # raise

  
  


if __name__ == "__main__": 
  main();