import numpy as np
import datetime
from datetime import datetime
import sys

# For subject 0 (1113) the start time was 31/01/2025 15:47 and subject 1(1114) it was 21/01/2025 13:52.

experiment_duration = 30 # mins

def loadRawData(filename, fromTimestamp):
    outdata = []
    fs = 250 # Hz
    maxdtjitter = 1000 # ms

    # Load data using np.genfromtxt to handle comma-separated values
    data = np.genfromtxt(filename, delimiter=',',dtype=['uint64','float','float'])

    fromEpoch = np.int64(fromTimestamp.timestamp() * 1000)
    toEpoch = np.int64(fromEpoch + 1000 * 60 * experiment_duration);
    isFirst = True
    t = -1
    prevTs = -1
    
    for row in data:
        if (len(row) > 2):
            if (row[0] > fromEpoch):
                if row[0] < toEpoch:
                    currentTS = row[0]
                    if t < 0:
                        t = currentTS - fromEpoch
                    if prevTs > 0:
                        dt = currentTS - prevTs
                        if (dt > maxdtjitter):
                            print("Data not continous. dt=",dt,"At timestamp",currentTS,datetime.utcfromtimestamp(currentTS/1000.0))
                            return np.array(outdata)
                    a = np.array([t/1000.0, row[1], row[2]])
                    # print(a)
                    outdata.append(a)
                    t = t + 1000.0/fs
                    prevTs = currentTS

    if (len(outdata) < 1):
        for row in data:
            if (len(row) > 2):
                if (row[0] > fromEpoch):
                    print("There are NO timestamps for this period in the data")
                    print("We want from {}({}) to {}({}) but the 1st timestamp is at {}({}).".format(fromEpoch,datetime.utcfromtimestamp(fromEpoch/1000.0),
                                                                                         toEpoch,datetime.utcfromtimestamp(toEpoch/1000.0),
                                                                                         row[0],datetime.utcfromtimestamp(toEpoch/1000.0)))
                    return np.array([])

    return np.array(outdata)




def loadHRdata(filename, fromTimestamp):
    outdata = []
    timeout_discontinous = 10*1000 # secs

    # Load data using np.genfromtxt to handle comma-separated values
    data = np.genfromtxt(filename, delimiter='\t',dtype=['uint64','float'])

    fromEpoch = np.int64(fromTimestamp.timestamp() * 1000)
    toEpoch = np.int64(fromEpoch + 1000 * 60 * experiment_duration);
    isFirst = True
    prevTs = -1
    
    for row in data:
        if (len(row) > 1):
            if (row[0] > fromEpoch):
                if row[0] < toEpoch:
                    currentTS = row[0]
                    if prevTs > 0:
                        dt = currentTS - prevTs
                        if (dt > timeout_discontinous):
                            print("Data not continous. dt=",dt,"At timestamp",currentTS,datetime.utcfromtimestamp(currentTS/1000.0))
                            return np.array(outdata)
                    a = np.array([(currentTS - fromEpoch)/1000.0, row[1]])
                    # print(a)
                    outdata.append(a)
                    prevTs = row[0]

    if (len(outdata) < 1):
        for row in data:
            if (len(row) > 2):
                if (row[0] > fromEpoch):
                    print("There are NO timestamps for this period in the data")
                    print("We want from {}({}) to {}({}) but the 1st timestamp is at {}({}).".format(fromEpoch,datetime.utcfromtimestamp(fromEpoch/1000.0),
                                                                                         toEpoch,datetime.utcfromtimestamp(toEpoch/1000.0),
                                                                                         row[0],datetime.utcfromtimestamp(toEpoch/1000.0)))
                    return np.array([])

    return np.array(outdata)





if (len(sys.argv) < 4):
    print("Please specify the start date and the filename in the following form:")
    print("{} dd/mm/yyyy HH:MM:SS rawoutfile.tsv hroutfile.tsv".format(sys.argv[0]))
    quit(1)
    
fromTS = datetime.strptime(sys.argv[1]+" "+sys.argv[2],"%d/%m/%Y %H:%M:%S")
rawdata = loadRawData('adc_data.tsv', fromTS)
print("Number of datapoints raw:",len(rawdata))
np.savetxt(sys.argv[3],rawdata,delimiter='\t',fmt='%f')

HRdata = loadHRdata('attyshrv_heartrate.tsv', fromTS)
print("Number of datapoints HR:",len(HRdata))
np.savetxt(sys.argv[4],HRdata,delimiter='\t',fmt='%f')
