class CacheManager:
    def __init__(self, totalCache, blockSize, numberOfWays):
        self.totalCache = totalCache
        self.blockSize = blockSize
        self.numberOfWays = numberOfWays
        totalLines = self.totalCache / self.blockSize
        self.LinesOneWay = totalLines / self.numberOfWays
        self.Cache = self.createCache()
        self.total = 0
        self.miss = 0
    
    def trunMem(self, input):
        return input << 12
    
    def createCache(self):
        Cache = [[] for _ in range(self.numberOfWays)]
        for i in range(len(Cache)):
            Cache[i] = [[] for _ in range(self.LinesOneWay)]
            for j in range(self.LinesOneWay):
                Cache[i][j] = [0] * self.blockSize
        return Cache
    
    def CheckInCache(self, data, dMemLoc):
        self.total += 1
        x = dMemLoc % self.LinesOneWay
        for i in range(len(self.Cache)):
            for cacheItem in self.Cache[i][x]:
                if cacheItem[0] == dMemLoc:
                    return data
        self.miss += 1
        return -999
    
    def PutInCache(self, data, dMemLoc):
        x = dMemLoc % self.LinesOneWay
        save = -1
        for i in range(len(self.Cache)):
            for j, cacheItem in enumerate(self.Cache[i][x]):
                if cacheItem == 0:
                    save = [i, x, j]
        self.Cache[save[0]][save[1]][save[2]] = [dMemLoc, data]
        return self.Cache[random.randint(0, (self.numberOfWays - 1))][x][random.randint(0, self.blockSize - 1)]
        

cacheCheck = CacheManager(4096, 8, 1)
with open("test.memtrace", "r+") as file:
    for line in file:
        data = line.split(" ")
        if cacheCheck.CheckInCache(data[1], int(data[2])) == -999:
            cacheCheck.PutInCache(data[1], int(data[2]))

print(cacheCheck)
