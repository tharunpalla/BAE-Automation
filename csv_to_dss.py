from hec.script import MessageBox
from hec.heclib.dss import HecDss
from hec.heclib.util import HecTime
from hec.io import TimeSeriesContainer
import java
import csv

try :
    try :
        #print 'Jython version: ', sys.version
        NUM_METADATA_LINES = 3
        DSS_FILE_PATH = 'wrftst.dss'
        CSV_FILE_PATH = 'wrftst.csv'
        PART_A = 'UMB'
        TIME_INTERVAL = '3HOUR'
        PART_F = 'WRFDAY2'

        myDss = HecDss.open(DSS_FILE_PATH)
        csvReader = csv.reader(open(CSV_FILE_PATH, 'r'), delimiter=',', quotechar='|')
        csvList = list(csvReader)

        print ("csvList: ", csvList[0])
        
        numLocations = len(csvList[0]) - 1
        numValues = len(csvList) - NUM_METADATA_LINES # Ignore Metadata
        locationIds = csvList[1][1:]
        print ('Start reading', numLocations, csvList[0][0], ':', ', '.join(csvList[0][1:]))
        print ('Period of ', numValues, 'values')
        print ('Location Ids :', locationIds)

        for i in range(0, numLocations):
            print ('\n>>>>>>> Start processing ', locationIds[i], '<<<<<<<<<<<<')
            precipitations = []
            for j in range(NUM_METADATA_LINES, numValues + NUM_METADATA_LINES):
                p = float(csvList[j][i+1])
                precipitations.append(p)

            print ('Precipitation of ', locationIds[i], precipitations[:10])
            tsc = TimeSeriesContainer()
            # tsc.fullName = "/BASIN/LOC/FLOW//1HOUR/OBS/"
            tsc.fullName = '/' + PART_A + '/' + locationIds[i].upper() + '/PRECIP-INC//' + TIME_INTERVAL + '/' + PART_F + '/'

            print ('Start time : ', csvList[NUM_METADATA_LINES][0])
            start = HecTime(csvList[NUM_METADATA_LINES][0])
            tsc.interval = 24 * 60
            times = []
            for value in precipitations :
              times.append(start.value())
              start.add(tsc.interval)
            tsc.times = times
            tsc.values = precipitations
            tsc.numberValues = len(precipitations)
            tsc.units = "MM"
            tsc.type = "PER-CUM"
            myDss.put(tsc)

    except Exception, e :
        MessageBox.showError(' '.join(e.args), "Python Error")
    except java.lang.Exception, e :
        MessageBox.showError(e.getMessage(), "Error")
finally :
    myDss.done()
    print ('\nCompleted converting ', CSV_FILE_PATH, ' to ', DSS_FILE_PATH)