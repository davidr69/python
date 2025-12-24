#!/usr/bin/python3

import ast
import sys

_src = 'nautobot/jobs/command_runner.py'

def validate_job_file(src):
	with open(src, "r") as f:
		try:
			tree = ast.parse(f.read())
		except SyntaxError:
			print(f"Skipping {src}: Syntax Error")
			return

	group_name = None

	# Iterate through every top-level item in the file
	for node in tree.body:
		if group_name is None and isinstance(node, ast.Assign):
			for target in node.targets:
				if isinstance(target, ast.Name) and target.id == "name":
					group_name = node.value.value

					if not group_name.startswith("lavacro-"):
						print("Group name validation failed")
				#sys.exit(1)
			continue

		# We only care about Class Definitions
		if isinstance(node, ast.ClassDef):
            
			# Could be an exception class instead of a Job class
			is_job = any(
				isinstance(base, ast.Name) and base.id == "Job" 
				for base in node.bases
			)

			if is_job:
				process_job(node, src)

def process_job(node, src):
	class_name = node.name
	print(f"Checking Job Class: {class_name} in {src}")

	# Rule A: Class Name Convention
	if not class_name.endswith("-job"):
		print(f"  [ERROR] Class '{class_name}' must end with '-job'")

	# Rule B: Inspect internal attributes (metadata)
	# We look inside the class body for assignments like name = "..."
	for item in node.body:
		if isinstance(item, ast.Assign):
			for target in item.targets:
				if isinstance(target, ast.Name) and target.id == "name":
					# Extract the actual string value
					if isinstance(item.value, ast.Constant):
						job_ui_name = item.value.value
						# Example: Ensure the UI name doesn't exceed 50 chars
						if len(job_ui_name) > 50:
							print(f"  [ERROR] Job name '{job_ui_name}' is too long.")

validate_job_file(_src)
