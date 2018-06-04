import sys
from test import true_negative, true_positive, false_positive, false_negative

if len(sys.argv) == 0:
    print "Improper Usage: Please provide an argument!"
    sys.exit(2)

print '        Accuracy         '
print "-------------------------"
print ((true_positive + true_negative) / float(true_positive + true_negative + false_negative + false_positive)) * 100
print "-------------------------"

print '        Precision        '
print "-------------------------"
print (true_positive / float(false_positive + true_positive)) * 100
print "-------------------------"

print '         Recall          '
print "-------------------------"
print (true_positive / float(true_positive + false_negative)) * 100
print "-------------------------"

print '    Confusion Matrix     '
print "-------------------------"
print "TP: " + str(true_positive)
print "TN: " + str(true_negative)
print "FP: " + str(false_positive)
print "FN: " + str(false_negative)
print "-------------------------"
