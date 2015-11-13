'''
liveramp OA:

frog jump through fallen leaves to the other bank:
the fallen leaves time line is A
frog jump distance is D, leave out jump action time 
the distance between banks is X

question: return the earliest time the frog can jump 
to the other side by any ways.nor return -1.
eg.
[2],2,1 ->-1   [2],3,4 ->0    [1],2,1  ->0  

[1,2,3,4,5] 7,1 ->-1    [1,2,4,2,5],5,2 ->2

'''
'''
To solve this problem,by looking at array A, we need to find the earliest candidate leaf fallen where the 
frog can jump to the destination, then if we can judge this candidate leaf is reachable trough the former 
fallen leaves,the problem is solved, or we need to consider the next candidate leaf.
To limit the time complexity to O(N), we need to build a table that show the reachable relation for 
all leaves before judging the reachability one by one.
'''
class solution:
    def frogjump(self,A,x,D):
        if D>=x:
            return 0
        elif len(A)==0:
            return -1
        reachable=[False for i in range(len(A))]  #initiate reachable relation array between leaves
        self.buildreachable(A,D,reachable)  
        for i in range(len(A)):   # a candidate fallen leaf causing possible earlest time
            if A[i]+D>=x:
                if reachable[i]:
                    return i
        return -1       
    def buildreachable(self,A,D,reachable):  # build reachable relation of all leaves
        maxdis=D
        for i in range(len(A)):
            if maxdis>=A[i]:
                maxdis=max(A[i]+D,maxdis)  #greedily,update further reaching
                if maxdis>=A[i]:
                    reachable[i]=True
                    
                    
