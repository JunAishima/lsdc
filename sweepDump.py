#!/opt/conda_envs/lsdc_dev/bin/python
import lsdb1
import sys

startDate = sys.argv[1]
endDate = sys.argv[2]
fname = sys.argv[3]

lsdb1.printColRequestsByTimeInterval(startDate,endDate,fname)
