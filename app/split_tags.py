import re
import os.path

# simple-minded method to separate doujin filenames into characteristic tags
# tried pyparsing but decided wasn't worth the effort

data = """[Null (nyanpoun)] Unnamed [Strike Witches](English)(Trinity Translations).zip"""

# crop filename extension
data = os.path.splitext(os.path.basename(data))[0]

# substitute all brackets with pipes
data = re.sub('[\(\[\)\]\{\}]','|',data)

# split by pipes, dropping empty entries
tags = re.split('\|', data)
tags = filter(None, tags)

# Strip whitespace from tags
tags = [t.strip() for t in tags]

# return list of tags
print tags


