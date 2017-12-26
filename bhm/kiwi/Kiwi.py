from bhm.kiwi import kiwiPyRaw

class Kiwi:
    def __init__(self, modelPath = None, cacheSize = -1, numThread = 0, userDicts = []):
        if modelPath == None:
            print(__file__.rfind('\\'), __file__.rfind('/'))
            p = max(__file__.rfind('\\'), __file__.rfind('/'))
            modelPath = __file__[:p+1]
        self.inst = kiwiPyRaw.initKiwi(modelPath, cacheSize, numThread)
        if type(userDicts) == str: userDicts = [userDicts]
        for ud in userDicts:
            kiwiPyRaw.loadUserDictKiwi(self.inst, ud)
        kiwiPyRaw.prepareKiwi(self.inst)

    def analyzeN(self, text, topN):
        return kiwiPyRaw.analyzeKiwi(self.inst, text, topN)

    def analyze(self, text):
          return kiwiPyRaw.analyzeKiwi(self.inst, text, 1)[0][0]

    def __del__(self):
        kiwiPyRaw.closeKiwi(self.inst)

if __name__ == "__main__":
    kiwi = Kiwi('model/')
    print(kiwi.analyze('아버지가방에 들어가신다.'))