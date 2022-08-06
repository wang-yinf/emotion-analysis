import urllib.parse
def transform(name):
    name1 = urllib.parse.quote(name)
    return name1
print(transform('追风筝的人'))