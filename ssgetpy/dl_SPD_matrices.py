from query import search

result = search(nzbounds=(100000,1000000), isspd=True, limit=10000000000, dtype='real')
result.download(extract=True,destpath="./SPD")


