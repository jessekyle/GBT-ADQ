import subprocess

#subprocess.call(["cd", "cd Pictures", "open Desert.jpg"])

subprocess.getoutput(["cd", "cd Pictures", "open Desert.jpg"])
