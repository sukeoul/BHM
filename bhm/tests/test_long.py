import bhm, os

def test():
    b =  bhm.BanmalHajiMara()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open('introduce.txt','r',encoding='utf-8') as f:
        r = f.read()
    tospeak = b.Banmal_Haji_Mara(r.splitlines())
    for line in tospeak:
        print(line)
    return None

if __name__ == '__main__':
    test()

