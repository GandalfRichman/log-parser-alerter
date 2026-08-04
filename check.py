from logalert.parser import parse_file

entries, bad = parse_file("data/sample.log")
print(len(entries), "parsed,", bad, "malformed")
print(entries[0])