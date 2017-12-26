__author__ = 'Chanwoo Yoon'
__email__ = 'ycw9@yonsei.ac.kr'
__version__ = '0.0.0'

from . import *

import hgtk
import re, os
from bhm.kiwi import Kiwi
from bhm import data


class BanmalHajiMara:
    """
    BanmalHajiMara
    """
    def __init__(self, path = 'kiwi/model/'):
        """
        Load Kiwi and replacement data to memory.
        :param path: Initial path is relative path to kiwi models.
        """

        os.chdir(os.path.dirname( os.path.abspath( __file__ ) ))
        self.kiwi = Kiwi.Kiwi(path)
        self.replace = data.getdata()

    def Banmal_Haji_Mara(self, text):
        """
        Check the type of text, convert text, and return it.
        :param text: Whether String or List of String.
        :return: String or List of String converted.
        """
        if type(text) == list:
            res = []
            try:
                for sentence in text:
                    words = sentence.split(" ")
                    if len(words) >=2:
                        res.append(" ".join(words[:-1]) + " " + self.Mal_Gillge_Haeraing(" ".join(words[-1:]))[0])
                    else:
                        res.append(" ".join(words[:-2])+" "+ self.Mal_Gillge_Haeraing(words[-1])[0])
                return res
            except Exception :
                print("Exception!")
        elif type(text) == str:
            res = ""
            last = text[-2:]
            res+=text[:-2]+ self.Mal_Gillge_Haeraing(last)[0]
            return res
        else :
            print("Not supported")


    def Mal_Gillge_Haeraing(self, last, mode="use"):
        """
        Convert Korean down talk to honorific talk.

        Function doing actual convert.
        There are two distinct mode, 'use' and 'debug'
        'use' mode are for use of program.
        'debug' mode are for debuging the program.
        Showing lot more info.

        :param last: The text to be converted
        :param mode: Mode selection. Only 'debug' would make change in function
        :return: Converted text
        """

        # To signify spaces for after Jamo conversion
        tokens = self.kiwi.analyze(last.replace(" ","|"))

        # Removing obstructing Morphological factor
        dell = ('이', 'VCP')
        if tokens.count(dell)>0:
            tokens.remove(dell)

        # For debugging
        if mode == "debug":
            print("##입력된 문장의 형태소 : ", end="")
            print(tokens)

        # Key set of data set (Which was loaded from data.py)
        key = self.replace.keys()
        lk = list(key)
        result = []
        change =""

        # Replace if the Morphological token exists in key set.
        for token in tokens:
            if token in lk:
                change = token
                token = self.replace.get(token)
                if(type(token[0])==tuple):
                    result.append(token[0])
                    result.append(token[1])
                    continue
            result.append(token)

        # Jaso conversion using hgtk
        test =''
        for i in result:
            if ord(i[0][0]) == 4359:
                test += "ㅂᴥ"
            test += hgtk.text.decompose(i[0])

        # Restructuring sentence from jaso ordering.
        one_char = re.compile('ᴥ[ㅂㄴㄹ]ᴥ')
        if one_char.search(test):
            words = test.split('ᴥ')
            for idx in range(1,len(words)):
                # 앞 글자가 종성이 없음
                if len(words[idx]) == 1 and len(words[idx-1].replace('|',"")) == 2:
                    #앞 글자에 합침
                    words[idx - 1] = words[idx-1]+words[idx]
                    words[idx] = ""
                # 있음
                elif len(words[idx]) == 1 and len(words[idx-1].replace('|',"")) == 3:
                    shp = ['ㅆ','ㅍ','ㄱ','ㅄ','ㄶ']
                    ep = ['ㄹ']
                    if words[idx] == 'ㅂ' and len(words[idx - 1].replace('|', "")) == 3 :
                        if words[idx - 1][-1] in shp :
                            if words[idx].count("|") > 0:
                                words[idx] = "|습"
                            else:
                                words[idx ] = "습"
                            continue
                        else :
                            if words[idx].count("|") > 0:
                                words[idx] = "|입"
                            else:
                                words[idx] = "입"
                            # words[idx] = ""
                    elif words[idx] =='ㄴ' and len(words[idx-1].replace('|',"")) == 3 and words[idx - 1].endswith('ㄹ'):
                        if words[idx-1].count("|") >0 :
                            words[idx - 1] = "|" + words[idx - 1].replace("|","")[:2] + words[idx]
                        else :
                            words[idx - 1] = words[idx - 1][:2] + words[idx]
                        # 지움
                        words[idx] = ""
                    elif words[idx] =='ㄹ':
                        if words[idx].count("|") > 0:
                            words[idx] = "|일"
                        else:
                            words[idx] = "일"

            test = "ᴥ".join([x for x in words if x is not ""])+"ᴥ"
        # For cases which wasn't covered,
        test = self.makePretty(test)

        # For debugging
        if mode == "debug":
            print("##변환된 형태소 : ", end="")
            print(result)
            print("##자모 : ", end="")
            print(test)

        # Restore spaces in original string
        changed_string = hgtk.text.compose(test).replace("|"," ")

        # For debugging
        if mode == 'debug':
            return changed_string,result,tokens
        else : return changed_string,result

    def makePretty(self, line):
        """
        Convert the jaso orderings which wasn't properly covered by
        Jaso restructuring process of function Mal_Gillge_Haeraing
        :param line: jaso orderings which wasn't properly covered
        :return: Converted jaso ordering
        """
        test = line
        test = test.replace("ᴥㅎㅏᴥㅇㅏᴥ", "ᴥㅎㅐᴥ")
        test = test.replace("ㅎㅏᴥㅇㅏᴥㅇㅛᴥ", "ᴥㅎㅐᴥ")
        test = test.replace("ㅎㅏᴥㄴㅣᴥㄷㅏᴥ", "ㅎㅏㅂᴥㄴㅣᴥㄷㅏᴥ")
        test = test.replace("ㅎㅏᴥㅇㅏㅆᴥ", "ᴥㅎㅐㅆᴥ")
        test = test.replace("ㄴㅏᴥㅇㅏㅆᴥ", "ᴥㅎㅐㅆᴥ")
        test = test.replace("ㄱㅏᴥㅇㅏㅆᴥ", "ᴥㄱㅏㅆᴥ")
        test = test.replace("ㅇㅣᴥㄴㅣᴥ", "ᴥㄴㅣᴥ")
        test = test.replace("ㄴㅓㄹㄴᴥ","ㄴㅓㄴᴥ")
        test = test.replace("ㄱㅡᴥㄹㅓㅎᴥㅇㅓᴥ","ㄱㅡᴥㄹㅐᴥ")
        test = test.replace("ㅡᴥㅇㅏᴥ","ㅏᴥ")
        test = test.replace("ㄱㅓㄹᴥㄴㅏᴥㅇㅛᴥ", "ㄱㅓㄴᴥㄱㅏᴥㅇㅛᴥ")
        return test


    def consoleTestAndUpdate(self):
        """
        Console debugging. Also can add new data.
        :return: None
        """
        print("------------------콘솔테스트 실행------------------")
        while True:
            i = input("##다음 문장 (종료 -1): ")
            if i == '-1':
                print("------------------테스트 종료----------------------")
                break

            result = self.Mal_Gillge_Haeraing(i, mode="debug")
            print("##Output :", result[0])

            # Adding new Data
            add = input("##수정하시겠습니까?(Yes: y or ㅇ, No: Enter)")
            if add == 'y' or add == 'ㅇ':
                print()
                print("##어느걸 수정하시겠습니까? (1부터 %d) :" % len(result[2]), result[2])
                keyidx = int(input())-1
                newOne = input("##수정할 문구를 입력해주세요 : ")
                change = self.Mal_Gillge_Haeraing(newOne, mode="debug")
                print("##어느 것으로 수정하시겠어요? (1부터 %d , 취소 -1, customize 0) :" % len(change[2]), change[2])
                validx = int(input())-1
                if validx == -2 : continue
                if validx == -1 :
                    #customize
                    str = input("##글자 값을 입력해주세요 : ")
                    type = input("##형태소 값을 입력해주세요 : ")
                    temp = (str, type)
                    self.addData(result[2][keyidx], temp)
                    print("##---------데이터가 추가되었습니다 :", result[2][keyidx], temp)
                else:
                    self.addData(result[2][keyidx], change[2][validx])
                    print("##---------데이터가 추가되었습니다 :",result[2][keyidx], change[2][validx])
                self.replace = data.getdata()
            print()

    def addData(self, key, val):
        """
        Add new data to data.py.
        :param key: key to be added into Dictionary self.replace
        :param val: Value to be added into Dictionary self.replace
        :return: None
        """
        with open('data.py', 'r', encoding='utf-8') as f:
            data = f.read()

        lines = data.split("\n")
        lines[-2] += ','
        lines[-1] = "                    " + str(key) + ": " + str(val)
        with open('data.py', 'w', encoding='utf-8') as f:
            for i in range(len(lines)):
                f.write(lines[i] + "\n")
            f.write("                    }")
