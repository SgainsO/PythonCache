import math
import random
from collections import defaultdict

class CacheManager:
    def __init__(self, totalCache, blockSize, numberOfWays):
        self.totalCache = totalCache
        self.blockSize = blockSize
        self.numberOfWays = numberOfWays
        totalLines = (self.totalCache * 1024) // self.blockSize
        self.LinesOneWay = totalLines // self.numberOfWays
        self.saved = {}
        self.Cache = self.createCache()
        self.total = 0
        self.miss = 0
        self.hits = 0


    def retMissRate(self):
        return self.miss / self.total

    def getIndex(self, memLoc):
        offset_bits = int(math.log2(self.blockSize))
        mask = self.LinesOneWay - 1
        return (memLoc >> offset_bits) & mask

    def getTag(self, memLoc):
        offset_bits = int(math.log2(self.blockSize))
        index_bits = int(math.log2(self.LinesOneWay))
        return memLoc >> (offset_bits + index_bits)
    
    def removeOffset(self, input):
        return input >> int(math.log2(self.blockSize))

    def trunMem(self, input):
        return input & 0xFFFFFFFF
    
    def createCache(self):
        Cache = [[] for _ in range(self.numberOfWays)]
        for i in range(len(Cache)):
            Cache[i] = [[] for _ in range(self.LinesOneWay)]
            for j in range(self.LinesOneWay):
                Cache[i][j] = None

        
        
        return Cache
    
    def CheckInCache(self, data, dMemLoc):
        self.total += 1
        x = self.getIndex(dMemLoc)
        tag = self.removeOffset(dMemLoc)
        for i in range(len(self.Cache)):
            if self.Cache[i][x] != None and self.Cache[i][x][0] == tag:
                self.updateLeastRecentlyUsed(x, tag)
                self.hits += 1
                return 1
        print(x)
        print(tag)
        self.miss += 1
        return -999
    
    def PutInCache(self, data, dMemLoc):
        x = self.getIndex(dMemLoc)
        save = -1
        tag = self.removeOffset(dMemLoc)

        highest = -1
        saveMem = 0

        for i in range(len(self.Cache)):
            cacheItem = self.Cache[i][x]
            print(cacheItem)
            if cacheItem != None and cacheItem[1] != '0':
                print("found")
            if cacheItem == None:
                save = [i, x]
                self.Cache[save[0]][save[1]] = [tag, data]
                self.updateLeastRecentlyUsed(x, tag)
                print("-")
                return
        print(tag, data)
        ind = self.getLeastRecentlyUsed(x, tag)
        self.Cache[ind][x] = [tag, data]
        self.updateLeastRecentlyUsed(x, tag)
        print("------")
        return
    
    def updateLeastRecentlyUsed(self, index, tag):
        if index not in self.saved:
            self.saved[index] = [[0, 0] for _ in range(self.numberOfWays)]
            self.saved[index][0] = [tag, 1]
            return 0
        usedArr = self.saved[index]
        for i, (t, u) in enumerate(usedArr):
            if t == tag:
                usedArr[i] = [tag, max([item[1] for item in usedArr]) + 1]

        
    def getLeastRecentlyUsed(self, index, tag):
        if index not in self.saved:
            self.saved[index] = [[0, 0] for _ in range(self.numberOfWays)]
            self.saved[index][0] = [tag, 1]
            return 0
        else:
            mini = float('inf')
            minIndex = -1
            for i in range(len(self.saved[index])):
                if self.saved[index][i][1] < mini:
                    mini = self.saved[index][i][1]
                    minIndex = i
            return minIndex
        
    def printResults(self):
        hit_count = self.total - self.miss
        miss_count = self.miss
        total_instructions = self.total
        miss_rate = self.retMissRate() * 100

        num_offset_bits = int(math.log2(self.blockSize))
        print(self.LinesOneWay)
        num_index_bits = int(math.log2(self.LinesOneWay))
        num_tag_bits = 32 - num_offset_bits - num_index_bits

        if self.numberOfWays == 1:
            associativity = "direct-mapped associativity"
        elif self.numberOfWays == self.LinesOneWay * self.numberOfWays:
            associativity = "fully associative"
        else:
            associativity = f"Number of ways = {self.numberOfWays}"

        print(f"Cache Size = {self.totalCache} KB")
        print(f"Block Size = {self.blockSize} B")
        print(f"{associativity}")
        print(f"Number of Victim Cache = 0")
        print(f"numOfOffsetBits = {num_offset_bits}")
        print(f"numOfIndexBits = {num_index_bits}")
        print(f"numOfTagBits = {num_tag_bits}")
        print(f"Cache hit count= {hit_count}")
        print(f"Cache miss count = {miss_count}")
        print(f"Instruction count = {total_instructions}")
        print(f"Cache miss rate = {miss_rate:.2f}%")


cacheCheck = CacheManager(32, 4, 1)
with open("test.memtrace", "r+") as file:
    for line in file:
        data = line.split(" ")
        data[2] = cacheCheck.trunMem(int(data[2], 16))
        if cacheCheck.CheckInCache(data[1], data[2]) == -999:
            cacheCheck.PutInCache(data[1], data[2])

print(cacheCheck.printResults())
