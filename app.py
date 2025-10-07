### Cache Block Size 8. Total Cache Size 4096

class CacheManager:
    def __init__(self, totalCache, blockSize, numberOfWays):
        self.totalCache = totalCache
        self.blockSize = blockSize
        self.numberOfWays = numberOfWays
        totalLines = self.totalCache / self.blockSize
        self.LinesOneWay = totalLines / self.LinesOneWay
        self.Cache = self.createCache()

    def trunMem(self, input):
        return input << 12

    def createCache(self):
        Cache = [[] * self.numberOfWays]
        while i in range(len(Cache)):
            Cache[i] = [] * self.LinesOneWay
            while j in range(self.LinesOneWay):
                Cache[i][j] = [0] * self.blockSize
        return Cache

    def CheckMemoryInCache(self, data, dMemLoc):
        x = dMemLoc % self.LinesOneWay 
        for i in range(len(self.Cache[self.numberOfWays])):
            for cacheItem in self.Cache[i][x]:
                if cacheItem[1] == data:
                    return data
                
    def PutInCache(self, data, dMemLoc):
        x = dMemLoc % self.LinesOneWay 
        save = -1
        for i in range(len(self.Cache[self.numberOfWays])):
            for j, cacheItem in enumerate(self.Cache[i][x]):
                if cacheItem[1] == data:
                    return False #Already In Cache
                elif cacheItem == 0:
                    save = [i, x, j]
        self.Cache[save[0]][save[1]][save[2]] = [dMemLoc, data]



    
