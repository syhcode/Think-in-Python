'''
FOR PFF:
in random 0-120 different page totally 10,000 references, and F change from 10 to 100 :

I got total page fault change from 3706 to 121(at F = 59 ),
thus the totoal page fault always decrease with F increase since the larger F maintain more page in resident set.
'''

def PFF(F):
    path = raw_input("please input file path for PFF: ")
    #path = "C:\\Users\\Administrator\\Desktop\\text2.txt"
    f=open(path)
    totalPage=int(f.readline())
    countPageFault=0
    lastPageFault=0
    resident={}
    maxResidentSize=0;
    minResidentSize=121;
    for countTime in range(1,totalPage+1):      
        reference = f.readline()
        if reference not in resident and countTime - lastPageFault<F:
            lastPageFault=countTime
            countPageFault+=1      
        if reference not in resident and  countTime - lastPageFault>=F:
            lastPageFault=countTime
            countPageFault+=1
            for key in resident.keys():
                if resident[key] == 1:
                    resident[key] = 0
                else:
                    del resident[key]
        resident[reference]=1
        maxResidentSize=max(maxResidentSize,len(resident)) 
        if(countTime>totalPage*0.1):
            minResidentSize=min(minResidentSize,len(resident))
    f.close()                                 
    print "total page fault :" + str(countPageFault) +"\n"
    print "minimum number of frames : "  + str(minResidentSize) +"\n"
    print "maximum number of frames : "+ str(maxResidentSize)+ "\n"

'''
FOR VSWS:
with the same file test for PFF,
First I keep M=100,Q=50, L change from 200 to 1000, the total page fault decrease from 1004 to 121( at L=334 )
Second I keep L=1000,Q=20, M change from 40 to 500, the total page fault decrease from 7194 to 121( at M=92)
Third I keep M=200, L=1000, Q change from 5 to 100 , the total page fault decrease from 1012 to 121( at Q=21)

In VSWS,thus the larger M and the larger distance between M and L will maintain more pages in resident set and thus casue fewer page faults,
meanwhile the larger fault tolerance, Q, will also maintain more pages in resident set and cause fewer page faults.
'''


def VSWS(M,L,Q):
    path = raw_input("please input file path for VSWS: ")
    #path = "C:\\Users\\Administrator\\Desktop\\text2.txt"
    f = open(path)
    totalPage=int(f.readline())
    countPageFault = 0
    lastSampleTime = 0
    lastFaultCount = 0
    resident={}
    maxResidentSize=0;
    minResidentSize=121;  
    for countTime in range(totalPage):
        if countTime - lastSampleTime >= L:
            lastSampleTime = countTime
            lastFaultCount = countPageFault
            for key in resident.keys():
                if resident[key] == 1:
                    resident[key] = 0
                else:
                    del resident[key]
        elif countPageFault - lastFaultCount >= Q  and  countTime - lastSampleTime >= M :
            lastSampleTime=countTime
            lastFaultCount = countPageFault
            for key in resident.keys():
                if resident[key] == 1:
                    resident[key] = 0
                else:
                    del resident[key]                  
        reference = f.readline()
        if reference not in resident:
            countPageFault+=1          
        resident[reference]=1
        maxResidentSize=max(maxResidentSize,len(resident)) 
        if(countTime>totalPage*0.1):
            minResidentSize=min(minResidentSize,len(resident))
    f.close()                  
    print "total page fault :" + str(countPageFault) +"\n"
    print "minimum number of frames : "  + str(minResidentSize) +"\n"
    print "maximum number of frames : "+ str(maxResidentSize)+ "\n"
'''
finally,for my built test file, for PFF I use loop to find parameter F, and I choose F=29, and it get that the relative
low page fault(853) and get  minimum frames allocated of 49 and maximum  frames allocated of 121;

for VSWS, with the same test file, I use nested loop to find parameter M,L,Q, and I choose M=63, L= 211, Q=30, and 
it get the relative low page fault(667),and get minimum frames allocated of 47 and maximum  frames allocated of 121;

'''
             
                
                
            
            
            
        
    