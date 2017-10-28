import argparse
import json
import re

common_unicode_conversion = {
	"\u2018": "'",
	"\u2019": "'"
}
# regex for different styles
style = {
	"link": "\[([^\(\)\[\]\!]+)\]\(([^\(\)\[\]\!]+)\)",
	"image": "!\[([^\(\)\[\]\!]*)\]\(([^\(\)\[\]\!]+)\)",
	"bold": "(?:\*{2}([^\s].*?[^\s]|[^\s])\*{2})|(?:_{2}([^\s].*?[^\s]|[^\s])_{2})", 
	"italic": "(?:\*([^\s].*?[^\s]|[^\s])\*)|(?:_([^\s].*?[^\s]|[^\s])_)", 
	"code": "`.+?`",
	"orderedList": "\s*^\s*\d+\.\s",
	"iframe": "<iframe.+>(.*)</iframe>",
	"class": "<iframe.+class=['\"](.*?)['\"].*>.*"
}
for k in style:
	style[k] = re.compile(style[k])

def is_comment(line):
	line = line.strip()
	return '<!--' in line or '-->' in line

def content_to_keep(line):
	if type(line) is not str:
		return False
	line = line.strip()
	return len(line) > 0 and not is_comment(line)

def replace_unicode(line):
	for k in common_unicode_conversion:
		line = line.replace(k, common_unicode_conversion[k])
	return line

def divider(line):
	if len(line.strip().replace("-","")) != 0:
		raise Exception("Invalid divider format: {0}".format(line))
	return "<hr>"

def bold(content, prefix_free=False):
	if not prefix_free:
		content = content.strip()[2:-2].strip()
	return "<b>{0}</b>".format(content.strip())

def italicize(content):
	return "<i>{0}</i>".format(content.strip()[1:-1].strip())

def code(content, prefix_free=False, pre_enabled=False, code_language=""):
	if not prefix_free:
		content = content.strip()[1:-1]
	if pre_enabled:
		format_str = "<pre><code class='{0}'>{1}</code></pre>"
	else:
		format_str = "<code class='{0}'>{1}</code>"
	return format_str.format(code_language, content)

def link(content):
	# assume it's not an image
	content = content.strip()
	try:
		data = style['link'].findall(content)
		# WARNING: only the first link is returned
		text = data[0][0]
		url = data[0][1]
		return "<a href='{0}' target='blank'>{1}</a>".format(url, text)
	except Exception as e:
		raise Exception("Invalid link format: {0}".format(content))

def headings(line):
	res = {
		"class": "lead",
		"content": ""
	}
	line = line.strip()
	try:
		i = 0
		while i < len(line) and line[i] == "#":
			i += 1
		line = line[i:]
		res['content'] = bold(line, prefix_free=True)
		return res
	except Exception as e:
		raise Exception("Invalid headings format: {0}".format(line))

def image(line):
	res = {
		"type": "image",
		"url": ""
	}
	line = line.strip()
	try:
		data = style['image'].findall(line)
		# WARNING: only the first image is returned
		if len(data[0][0].strip()) > 0:
			res['caption'] = data[0][0]
		res['url'] = data[0][1]
		return res
	except Exception as e:
		raise Exception("Invalid image format: {0}".format(line))

def block(line):
	line = line.strip()
	if line[0] != '>':
		raise Exception("Invalid blockquote format: {0}".format(line))
	line = line[1:].strip()
	return '<blockquote>{0}</blockquote>'.format(line)

def ordered_list(values):
	return {
		"type": "ordered-list",
		"content": values
	}

def unordered_list(values):
	return {
		"type": "unordered-list",
		"content": values
	}

style_function = {
	"link": link,
	"image": image,
	"bold": bold, 
	"italic": italicize,
	"code": code,
	"ordered_list": ordered_list,
	"unordered_list": unordered_list
}


def htmlfy(line):
	for key in ["bold", "italic", "link",  "code"]:
		match = style[key].search(line)
		while match is not None:
			line = line[:match.start()] + style_function[key](match.group()) + line[match.end():]
			match = style[key].search(line)
	return line

def iframe(d):
	d = d.strip()
	container = "<div class='row'><div class='col-sm-8 col-sm-offset-2 text-center'>{0}</div></div>"
	container2 = "<div class='embed-video-container embed-responsive embed-responsive-16by9' style='margin-bottom:0px'>{0}</div>"

	match = style['iframe'].match(d)
	word = htmlfy(match.groups()[0])
	content = d.replace(word, "") 

	match2 = style['class'].match(content)
	if match2 is not None and 'embed-responsive-item' in match2.groups()[0]:
		content = container2.format(content)

	content = container.format(content + word)
	return content

def process(d):
	"""Process general information, except multiple line code/list"""
	# image
	if len(d) >= 5 and d[:2] == '![':
		return image(d)
	# heading
	elif d[0] == "#":
		return headings(htmlfy(d))
	# block
	elif d[0] == ">":
		return block(d)
	elif d[:3] == "---":
		return divider(d)
	else:
		return htmlfy(d)

def creat_json(file):
	# read in the file
	with open(file, "r") as f:
		data = f.read().strip().split("\n")
	# filter out empty lines and comments
	data = list(filter(content_to_keep, data))
	# replace common unicode with english characters
	data = list(map(replace_unicode, data))
	# deal with pre-formated code first
	code_multiple_line_detected = False
	code_language = ""
	code_block_so_far = []
	new_data = []
	for d in data:
		if len(d.strip()) >= 3 and d.strip()[:3] == '```':
			if code_multiple_line_detected:
				code_multiple_line_detected = False
				new_data.append(code("\n".join(code_block_so_far), prefix_free=True, pre_enabled=True, code_language=code_language))
				code_block_so_far = []
			else:
				code_multiple_line_detected = True
				code_language = d.strip()[3:].strip()
				continue
		elif code_multiple_line_detected:
			code_block_so_far.append(d)
		else:
			new_data.append(d)
	if code_multiple_line_detected:
		new_data.append(code("\n".join(code_block_so_far), prefix_free=True))
	data = new_data
	# strip leading and trailing empty spaces for all non-empty text
	data = list(map(lambda x: x.strip(), data))
	res = list()
	# process data
	ordered_list_detected = False
	ordered_list_so_far = []
	unordered_list_detected = False
	unordered_list_so_far = []
	for d in data:
		if "<pre>" in d and "</code>" in d:
			res.append(d)
			continue
		if len(d) >= 2 and (d[:2] == '- ' or d[:2] == '* '):
			if ordered_list_detected:
				ordered_list_detected = False
				res.append(ordered_list(ordered_list_so_far))
				ordered_list_so_far = []
			unordered_list_detected = True
			unordered_list_so_far.append(process(d[2:].strip()))
		elif style['iframe'].search(d) is not None:
			res.append(iframe(d))
		elif style['orderedList'].search(d) is not None:
			if unordered_list_detected:
				unordered_list_detected = False
				res.append(unordered_list(unordered_list_so_far))
				unordered_list_so_far = []
			ordered_list_detected = True
			match = style['orderedList'].search(d)
			ordered_list_so_far.append(process(d[match.end():].strip()))
		else:
			if ordered_list_detected:
				ordered_list_detected = False
				res.append(ordered_list(ordered_list_so_far))
				ordered_list_so_far = []
			elif unordered_list_detected:
				unordered_list_detected = False
				res.append(unordered_list(unordered_list_so_far))
				unordered_list_so_far = []
			res.append(process(d))
	if ordered_list_detected:
		ordered_list_detected = False
		res.append(ordered_list(ordered_list_so_far))
	elif unordered_list_detected:
		unordered_list_detected = False
		res.append(unordered_list(unordered_list_so_far))
	# save file
	saveName = "{0}.json".format(file.split(".")[0])
	with open(saveName, "w") as f:
		json.dump({"blog-content": res}, f, indent=2)
	return saveName


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="a parser that converts a text file to a json file according to stac blog content guideline")
	parser.add_argument("source", type=str, help="<name>.txt")
	args = parser.parse_args()

	try:
		print("json file saved as {0}".format(creat_json(args.source)))
		print("SUCCESS")
	except Exception as e:
		print("FAILED\n")
		print(e)
