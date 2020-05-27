#!/usr/bin/env python3
import os
import re

SOURCE_FILES_DIR="scrapy/files/"
PARSED_FILES_DIR="scrapy/parsed_files/"
HTML_TAGS_PATTERN="<.[^>]*>"
DOUBLE_LINE_BREAKS_PATTERN="\n\n"
for filename in os.listdir(SOURCE_FILES_DIR):
	with open(SOURCE_FILES_DIR + filename, "r") as f:
		file_content = f.read()
		replace_result = re.sub(HTML_TAGS_PATTERN, '', file_content)
		replace_result = re.sub(DOUBLE_LINE_BREAKS_PATTERN, '', replace_result)
		with open(PARSED_FILES_DIR + filename, "w") as f2:
			f2.write(replace_result)
