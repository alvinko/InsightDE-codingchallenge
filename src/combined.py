'''
Word Count and Running Median
'''

import string, glob, time, sys, os

start = time.time()

#Define running median function

from heapq import heappush, heappushpop

def running_median():
    def gen():
        left, right = [], [(yield)]
        while True:
            heappush(left,  -heappushpop(right, (yield right[0])))
            heappush(right, -heappushpop(left, -(yield ((right[0] - left[0])/2.0))))
    g = gen()
    next(g)
    return g

stream = running_median()

#Define process flow functions

def processBoth():
    for file in files:
        print "Current File Being Processed is: " + file

        f = open(file, "r")

        for line in f:
            words = line.split()
            mList.append(len(words))

            for word in words:
                word = word.translate(string.maketrans("",""), string.punctuation).lower()

                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1

        f.close()

def processWC():
    for file in files:
        print "Current File Being Processed is: " + file

        f = open(file, "r")

        for line in f:
            words = line.split()

            for word in words:
                word = word.translate(string.maketrans("",""), string.punctuation).lower()

                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1

        f.close()

def processRM():
    for file in files:
        print "Current File Being Processed is: " + file

        f = open(file, "r")

        for line in f:
            words = line.split()
            mList.append(len(words))

        f.close()

#Define process flow arguments
if len(sys.argv) != 4:
    print "Incorrect arguments passed"
    print "1st argument - mode - 0 (word count), 1 (running median), 2 (both)"
    print "2nd argument - input directory"
    print "3rd argument - output directory"
    sys.exit()

cwd         = os.getcwd()
mode        = int(sys.argv[1])
input_dir   = "%s/%s" % (cwd, sys.argv[2])
output_dir  = "%s/%s" % (cwd, sys.argv[3])

if not os.path.exists(input_dir):
    print "Invalid input directory"
    sys.exit()

if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
    except OSError:
        print "Invalid output directory"
        sys.exit()

# Define global paths
path = '%s/*.txt' % input_dir
files = sorted(glob.glob(path))

if len(files) < 1:
    print "No files found"
    sys.exit()

wordcount={}
mList = []

if mode == 0:
    processWC()
elif mode == 1:
    processRM()
elif mode == 2:
    processBoth()
else:
    print "Bad mode - 0 (word count), 1 (running median), 2 (both)"
    sys.exit()

if mode:
    out_file_med=open('%s/med_result.txt' % output_dir, 'w')
    for n in mList:
        out_file_med.write("%s \n" % str(stream.send(n)))
    out_file_med.close()

out_file_wc=open('%s/wc_result.txt' % output_dir, 'w')

for k, v in wordcount.items():
    out_file_wc.write("%s %d\n" % (k, v))

out_file_wc.close()

end = time.time()

print "Total runtime (in seconds): " + str(end-start)