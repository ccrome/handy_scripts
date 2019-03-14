import argparse
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


p = argparse.ArgumentParser()
p.add_argument("filename", help="Filename of component report from Altium.  Something like SchLib1.cmp")

args = p.parse_args()
pins = open(args.filename, "r").readlines()
pins = [re.sub(" +", " ", x ) for x in pins] # eliminate multiple spaces
pins = [x.strip() for x in pins]             # eliminate leading and trailing whitespace
pins = [x for x in pins if x != ""] # Remove blank lines
matching_to_remove = ["Component Name", "Hidden Pins", "Part : ", "Pins - ", "Part Count :"]
for m in matching_to_remove:
    pins = [x for x in pins if not x.startswith(m)]

pins_x = list()
for pin in pins:
    m = re.match("^([^ ]+) ([^ ]+) ([^ ]+)$", pin)
    pins_x.append("%s %s" % (m.group(2), m.group(1))) # Spit both pin name and number out for debugging
pins = pins_x
pins.sort(key = natural_keys)

pins_x = list()
for pin in pins:
    m = re.match("^([^ ]+) ([^ ]+)$", pin)
    pins_x.append(m.group(2))
pins = pins_x

fn = "%s.txt" % args.filename
f = open(fn, "w")
for pin in pins:
    f.write("%s\n" % pin)
f.close()
print("Success:  Pins written to %s" % fn)
