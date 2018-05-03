#coding: utf-8
import sys
import c_path

MAP_1 = [
0, 0, 0, 0, 1, 1, 0, 1, 1, 0,
0, 0, 0, 0, 1, 1, 0, 0, 0, 0,
0, 0, 0, 1, 0, 1, 1, 1, 1, 0,
0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
]

posList = []
blockList=[]
for i in range(10):
    for j in range(10):
        posList.append( (i,j, 1+MAP_1[i*10+j] ) )
        if MAP_1[i*10+j] == 1:
            blockList.append( (i,j) )

pos = [(0,0,1),(0,1,1),(1,0,1),(1,1,1)]
block = [(0,0)]
c_path.CreateMap(2,2,pos,block)

print("blockList is ",blockList)
c_path.CreateMapByBlock(10,10,blockList)

print("posList is ",posList)
c_path.CreateMapByCost(10,10,posList)

def test():
    cost, result = c_path.SeekPath( (0,0), (8,7) )
    pList=list(result)
    pos_list = []
    while pList:
        x = pList.pop(0)
        y = pList.pop(0)
        pos_list.append( (x,y) )
    return cost, pos_list

if False:
    for i in range(10):
        print(">>>>>>>>>>>>>>>>>>>>>>     run test  ",i)
        pos_list = test()

cost, pos_list = test()
print("cost: %s \npos_list is: %s"%(cost,str(pos_list)))

print("test finished")
c_path.DeleteMap()
print("finished")
