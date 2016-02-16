'''
Created on Nov 16, 2015

@author: Siyu Huo
'''

'''
Finally run csefsck() in __main__, I got check result:

cse fuse devId is 20, correct!

time information in block 26, mtime is wrong!

time information in block 30, mtime is wrong!

block 6166 is missing in free block list 16
block 6167 is missing in free block list 16
block 6168 is missing in free block list 16
block information is missing in free block list! 

 '.' item in directory block30 is wrong!

indrect message in inode block 27 is wrong!



'''

import time
import os
 
def csefsck():
    
    #get super block information first
    path=inputPath;
    f=open(path+"\\fusedata.0")
    line=f.readline()
    contents=line.split(",")
    creatTime0=contents[0].split(":")[1][1:]
    mounted0=contents[1].split(":")[1]
    devId0=contents[2].split(":")[1]
    freeStart0=contents[3].split(":")[1] 
    freeEnd0= contents[4].split(":")[1]
    root0= contents[5].split(":")[1]
    maxBlocks0=contents[6].split(":")[1][:-1]
    
    #the top-down check method begin from root directory, in recursive way.
          
    cse_checkId(devId0)
    cse_timelogic(root0)
    cse_blockinfo(path,freeStart0,freeEnd0,maxBlocks0)
    cse_dircheck('25',root0)
    cse_dirlink(root0)
    cse_arraycheck(root0)
    cse_sizecheck(root0)
       
def cse_checkId(devId0):   
    if devId0!='20':
        print "this filesystem id is wrong!\n"
    else:
        print "cse fuse devId is "+devId0+', correct!\n'   
         
def cse_timelogic(block_num): #compare time using UNIX Epoch time (ISO 8601) 
    node_info=getNode(block_num)
    curtime=time.time()
    atime=float(node_info[4].split(':')[1])
    ctime=float(node_info[5].split(':')[1])
    mtime=float(node_info[6].split(':')[1])   
    if  atime>curtime:
        print "time information in block "+ block_num+", "+"atime "+ "is wrong!\n" 
    if  ctime>curtime :
        print "time information in block "+ block_num+", "+"ctime "+"is wrong!\n" 
    if  mtime>curtime:
        print "time information in block "+block_num+", "+"mtime "+"is wrong!\n"  
        
    info=getInode(block_num) #get filename_to_inode_dict
    if len(info)>0: # judge directory
        for subinfo in info:
            temp=subinfo.split(":")
            if temp[0]=='d' and temp[1]!='.'and temp[1]!='..':
                cse_timelogic(temp[2])
            if temp[0]=='f':
                node_info=getNode(temp[2])
                atime=float(node_info[5].split(':')[1])
                ctime=float(node_info[6].split(':')[1])
                mtime=float(node_info[7].split(':')[1])
                if  atime>curtime:
                    print "time information in block "+ temp[2]+", "+"atime "+ "is wrong!\n" 
                if  ctime>curtime :
                    print "time information in block "+ temp[2]+", "+"ctime "+"is wrong!\n" 
                if  mtime>curtime:
                    print "time information in block "+ temp[2]+", "+"mtime "+"is wrong!\n"         
                   
            
def cse_blockinfo(path,freeStart0,freeEnd0,maxBlocks0): # check by used block + free block = maxblock
    usedBlock=getUsedBlock(path)
    checkblock=usedBlock[-1]+1
    freesum=0
    for i in range(int(freeStart0),int(freeEnd0)+1):
        freeBlock=getFreeList(path,i)
        freesum+=len(freeBlock)
        for k in freeBlock:
            while int(k)!=checkblock and checkblock<10000:
                print "block "+str(checkblock)+" is missing in free block list "+str(i)
                checkblock+=1
            if k in usedBlock:
                print "error: block " +k+" used but in free block list!\n"
            checkblock+=1                    
    if len(usedBlock)+freesum!=maxBlocks0:
        print "block information is missing in free block list! \n"          

def cse_dircheck(pre_num,cur_num): #block number check with directory 
    checkcount=0
    info=getInode(cur_num)
    if len(info)>0:
        for subinfo in info:
            temp=subinfo.split(':')
            if temp[0]=='d' and temp[1]=='.' and temp[2]==cur_num:
                checkcount+=1
            if temp[0]=='d' and temp[1]=='.' and temp[2]!=cur_num:
                checkcount+=1
                print " '.' item in directory block" + cur_num+" is wrong!\n"   
            if temp[0]=='d' and temp[1]=='..' and temp[2]== pre_num:
                checkcount+=1
            if temp[0]=='d' and temp[1]=='..' and temp[2]!= pre_num:
                checkcount+=1
                print " '..' item in directory block" + cur_num+" is wrong!\n" 
            if temp[0]=='d' and temp[1]!='.' and temp[1]!='..':
                cse_dircheck(cur_num, temp[2])
        if checkcount!=2:
            print "directory block "+ cur_num + " missing directory information!\n"
                        
def cse_dirlink(block_num): #link count check 
    inode_info=getInode(block_num)
    node_info=getNode(block_num)
    if len(inode_info)>0:
        if  len(inode_info)!=int(node_info[-1].split(":")[1]):
            print "directory block" +block_num+"link information is wrong!"
        for subinfo in inode_info:
            temp=subinfo.split(":")
            if temp[0]=="d" and temp[1]!='.' and temp[1]!='..':
                cse_dirlink(temp[2])
                      
def cse_arraycheck(block_num): #check indirect information in inode
    info=getInode(block_num)
    if len(info)>0:
        for subinfo in info:
            temp=subinfo.split(":")
            if temp[0]=='d' and temp[1]!='.' and temp[1]!='..':
                cse_arraycheck(temp[2])
            elif temp[0]=='f':
                node_info=getNode(temp[2])        
                block_pos=node_info[-1].split(":")[-1]
                indirect= node_info[-1].split(' ')[0].split(":")[1]
                f=open(path+block_pos)
                line=f.readline()
                if len(line.split(", "))<2 and indirect=='1' :
                    print "indrect message in inode block "+temp[2]+" is wrong!\n"
                        
def cse_sizecheck(block_num): #check size and indirect information in inode
    info=getInode(block_num)
    if len(info)>0:
        for subinfo in info:
            temp=subinfo.split(":")
            if temp[0]=='d' and temp[1]!='.' and temp[1]!='..':
                cse_sizecheck(temp[2])
            elif temp[0]=='f':
                node_info=getNode(temp[2])        
                block_pos=node_info[-1].split(":")[-1]
                indirect= node_info[-1].split(' ')[0].split(":")[1]
                fsize= int(node_info[0].split(":")[1])
                if indirect =='0':                    
                    if fsize>4096:
                        print "size message in inode block "+block_num+" is wrong!\n"
                if indirect== '1':
                    f=open(path+block_pos)
                    line=f.readline()
                    content=line.split(", ")
                    if not (len(content)*4096>fsize and (len(content)-1)*4096<fsize):
                        print "size message in inode block "+block_pos+" is wrong!\n"
                           
def getUsedBlock(path): 
    dirs=os.listdir(path)
    arrayblocks=[]
    for dirinfo in dirs:
        arrayblocks.append(int(dirinfo.split('.')[1]))
    return sorted(arrayblocks)

def getFreeList(path,block_num):
    temp_path=path+"\\fusedata."+str(block_num)
    f=open(temp_path)
    line=f.readline()
    freelist = line.split(', ')
    return freelist 
    
    
def getInode(block_num): #get filename_to_inode_dict information in directory
    f=open(path+block_num)
    line=f.readline()
    content1=line.split("{")
    if len(content1)==3:
        content1=content1[2][:-2]
        content2=content1.split(", ")
        return content2
    else:
        return []
    
def getNode(block_num): # for directory get the information except  filename_to_inode_dict, for the inode get all info
    f=open(path+block_num)
    line=f.readline()
    content=line.split("{")
    if len(content)==3:
        content1=content[1]
        content2=content1.split(", ")[:-1]
        return content2
    else:
        content1=content[1][:-1]
        content2= content1.split(", ")
        return content2      
               
if __name__=="__main__":
    csefsck()         