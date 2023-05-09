
import pandas as pd
import numpy as np


class GradeBook:

    def __init__(self, GRADEBOOK="/home/faith/UIC_template/example.xlsx") -> None:

        namelistDF = pd.read_excel(GRADEBOOK)
        namelistDF = namelistDF.iloc[:, [0, 1, 2, 3]]

        studentnames = namelistDF['ename'].str.lower().str.split(expand=True)

        surname = studentnames.iloc[:, 0]  # .str.upper()
        firstname = studentnames.iloc[:, 1]  # .str.capitalize()
        namelistDF['name'] = firstname + surname
        namelistDF['firstname'] = firstname
        namelistDF['familyname'] = surname
        namelistDF['chinesename'] = namelistDF['cname']
        namelistDF['studentnum'] = namelistDF.iloc[:, 2].astype(
            'Int64').astype('str')  # .map(str) #.astype(str) #.apply(str)
        # namelistDF.studentnum.astype(str)

        self.studentDF = namelistDF[[
            'name', 'chinesename', 'studentnum', 'Session', 'familyname', 'firstname']]
        self.studentDF = self.studentDF.dropna()

        self.studentlist = self.studentDF.to_numpy()
        self.studentcnt = self.studentlist.shape[0]
        studentnames, cnt = np.unique(
            self.studentlist[:, 0], return_counts=True)
        self.duplicatename = studentnames[cnt > 1]
        self.duplicateinfo = self.studentlist[self.studentlist[:, 0]
                                              == self.duplicatename]
        
        self.duplicateinfo = np.insert(self.duplicateinfo, 1, values=['Jiahui Wang', 'Bernice'], axis=1)
        print("duplicateinfo", self.duplicateinfo, type(self.duplicateinfo))
        
        


    def checkIsDuplicate(self, name):
        ret = False
        for items in self.duplicateinfo:     
            if name in items[0]:
                return True

    def findStudentNumByName(self, name):
        try:
            currentStudentNo = int(
                self.studentDF.loc[self.studentDF['name'] == name]['studentnum'].to_numpy()[0])
            return currentStudentNo
        except:
            print(name, "not found!")
            return None

    def findStudentInfoBID(self, studentnum, info='firstname'):
        ret = []        
        try:
            studentnum = str(studentnum)
            firstname = str(
                self.studentDF.loc[self.studentDF['studentnum'] == studentnum][info].to_numpy()[0])
            ret.append(firstname)
            
            name = str(
                self.studentDF.loc[self.studentDF['studentnum'] == studentnum]['name'].to_numpy()[0])
            
            if self.checkIsDuplicate(name):

                # b = np.any(a[:, 1] == 5)
                # c = np.any(np.isin(a[:, 1], [2, 4, 6]))

                alias = str(
                self.duplicateinfo[self.duplicateinfo[:, 3] == studentnum][0][1])
                print(alias)
                ret.append(alias)
            return ret
        except:
            print(studentnum, "not found!")
            return ret

    def findStudentName(self, dirname):
        splits = dirname.split('_')
        # splits = os.path.basename(os.path.basename(os.path.dirname(code_file))).split('_')
        if len(splits) < 2:
            return None
        studentName, submissionId = splits[0], splits[1]
        if "(" in studentName:
            studentName = studentName[:studentName.index("(") - 1]
        studentName = studentName.replace(' ', '')
        studentName = studentName.lower()
        return studentName

if __name__ == "__main__":
    gb = GradeBook()
    # name = gb.findStudentName('Qidi SUN (ikun SUN)_1446817_assignsubmission_file_')
    
    # print(name)
    print(gb.findStudentInfoBID('2230026149'))
    # print(gb.findStudentNumByName('qidisun'))
    