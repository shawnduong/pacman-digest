#!/usr/bin/env python3

import json
import os
import shutil
import sys

from subprocess import check_output

ROOT = os.path.dirname(__file__)

def help_dialogue() -> int:

	s  = "Usage: ./main.py [OPTION]\n"
	s += "Generate visualizations of space usage for Linux systems using pacman.\n"
	s += "\n"
	s += "OPTIONS:\n"
	s += "  -h, --help  Display this help dialogue and exit.\n"
	s += "\n"
	s += "If no additional arguments are supplied, then pacman-usage will generate a\n"
	s += "'digest.html' file containing data visualizations. Run the program, then open\n"
	s += "up 'digest.html' in a browser to view data.\n"
	s += "\n"
	s += "Written by Shawn 'skat' Duong.\n"
	s += "GitHub: https://github.com/shawnduong/"

	print(s)

	return 0

def parse(data: str) -> list:
	"""
	Take the raw string data of a single package entry and return it
	represented as a list.
	"""

	output = {}        # {"Name": n, "Version": v, ...}
	buffer = ["", ""]  # [key, value]

	# Whitespace strip function.
	strip = lambda s: s.lstrip().rstrip()

	for line in data.split("\n"):

		# Save buffer to output, refresh buffer.
		if ":" in line and buffer[0] != "":
			output[buffer[0]] = buffer[1]
			buffer = ["", ""]

		# Parse data.
		if ":" in line:
			line = line.split(":")
			buffer[0]  = strip(line[0])
			buffer[1] += strip(line[1])
		else:
			buffer[1] += " "
			buffer[1] += strip(line[1])

	# Convert KiB, MiB, or GiB to B.
	size = output["Installed Size"]
	if "KiB" in size:
		output["Installed Size"] = float(size.split()[0])*(1024**1)
	elif "MiB" in size:
		output["Installed Size"] = float(size.split()[0])*(1024**2)
	elif "GiB" in size:
		output["Installed Size"] = float(size.split()[0])*(1024**3)

	# Remove irrelevant data and convert it all into a list to reduce size.
	return [
		output["Name"],
		output["Version"],
		output["Description"],
		output["Provides"].split("  "),
		output["Depends On"].split("  "),
		output["Optional Deps"].split("  "),
		output["Required By"].split("  "),
		output["Optional For"].split("  "),
		output["Conflicts With"].split("  "),
		output["Replaces"].split("  "),
		output["Installed Size"],
		output["Packager"],
		output["Build Date"],
		output["Install Date"],
		output["Install Reason"],
	]

def digest_data() -> int:
	"""
	Digest data and write to "digest.html" in the ROOT directory. The actual
	data visualization generation is handled in JS, and Python only writes the
	relevant data to "digest.html" for the JS to handle.
	"""

	# "pacman -Qi" gets list of packages and their info entries.
	cmd = lambda: check_output(["pacman", "-Qi"]).decode("utf-8").split("\n\n")

	# Compile a list of packages from the output of "pacman -Qi"
	packages = [parse(e) for e in cmd() if len(e) > 0]

	# Get the total, used, and free space (B) of the root partition.
	total, used, free = shutil.disk_usage("/")

	# Wrap up all data into a single JSON string.
	data = json.dumps({"packages": packages, "total": total, "used": used})

	# Read the template and substitute the data.
	with open(ROOT + "/template.html", "r") as f:
		html = f.read().replace("{{ DATA }}", data)

	# Read the stylesheet and substitute the CSS.
	with open(ROOT + "/css/style.css", "r") as f:
		html = html.replace("{{ CSS }}", f.read())

	# Read the jQuery and substitute the JS.
	with open(ROOT + "/js/jquery-3.6.0.slim.min.js", "r") as f:
		html = html.replace("{{ JQUERY }}", f.read())

	# Read the Chart.js and substitute the JS.
	with open(ROOT + "/js/chart.min.js", "r") as f:
		html = html.replace("{{ CHARTJS }}", f.read())

	# Read the JavaScript and substitute the JS.
	with open(ROOT + "/js/script.js", "r") as f:
		html = html.replace("{{ JAVASCRIPT }}", f.read())

	# Write to "digest.html"
	with open(ROOT + "/digest.html", "w") as f:
		f.write(html)

	print(":: Relevant data has been written to 'digest.html'")
	print(":: Open up 'digest.html' with a browser to see data visualizations.")

	return 0

def main(args):

	if len(args) == 1:
		return digest_data()

	elif "-h" in args or "--help" in args:
		return help_dialogue()

	else:
		print(":: Unknown usage. Try running './main.py --help' for more info.")

	return -1

if __name__ == "__main__":
	exit(main(sys.argv))
