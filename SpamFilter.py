from numpy import *
import math
import jieba


def Arrange(Input,Output,Range):
    Ram=open(Input,encoding="utf-8").readlines()
    fOut=open(Output,"w",encoding="utf-8")
    for i in Range:
        fOut.write(Ram[i])
    fOut.close()


def Train(HamDir,SpamDir,Output):
    print("Training Model...")
    RHam=open(HamDir,encoding="utf-8").read()
    RSpam=open(SpamDir,encoding="utf-8").read()
    RLHam=open(HamDir,encoding="utf-8").readlines()
    RLSpam=open(SpamDir,encoding="utf-8").readlines()

    HamWordC=0
    fOut=open("HamTrainCut.txt","w",encoding="utf-8")
    for i in RLHam:
        temp=jieba.lcut(i,cut_all=False)
        HamWordC+=len(temp)
        tempStr=""
        for j in temp:
            tempStr+=j+" "
        tempStr+="\n"
        fOut.write(tempStr)
    fOut.close()
    print("HamWordC="+str(HamWordC))

    SpamWordC=0
    fOut=open("SpamTrainCut.txt","w",encoding="utf-8")
    for i in RLSpam:
        temp=jieba.lcut(i,cut_all=False)
        SpamWordC+=len(temp)
        tempStr=""
        for j in temp:
            tempStr+=j+" "
        tempStr+="\n"
        fOut.write(tempStr)
    fOut.close()
    print("SpamWordC="+str(SpamWordC))

    FeatureList1=jieba.lcut(RHam+"\n"+RSpam,cut_all=False)
    FeatureList2=list(set(FeatureList1))
    fOut=open(Output,"w",encoding="utf-8")
    for i in FeatureList2:
        cjwt=0
        for j in RLHam:
            if j.find(i)!=-1:
                cjwt+=1
        PwcHam=(1+cjwt)/(2+len(RLHam))
        cjwt=0
        for j in RLSpam:
            if j.find(i)!=-1:
                cjwt+=1
        PwcSpam=(1+cjwt)/(2+len(RLSpam))
        fOut.write(i+" "+str(PwcHam)+" "+str(PwcSpam)+"\n")
    fOut.close()
    return HamWordC,SpamWordC










def LoadFeatureList(FeatureDir):
    FeatureList=open(FeatureDir,encoding="utf-8").readlines()
    try:
        for i in range(len(FeatureList)):
            FeatureList[i]=FeatureList[i].strip().split(" ")
            if len(FeatureList[i])!=3:
                del FeatureList[i]
            if FeatureList[i][0].strip()=="":
                del FeatureList[i]
            if type(FeatureList[i])==type("string"):
                del FeatureList[i]
            try:
                float(FeatureList[i][1])+float(FeatureList[i][2])
            except BaseException:
                del FeatureList[i]
    except BaseException:
        pass
    return FeatureList











def Iterate(Input,Output,SynonymDir,FeatureDir,Option):
    try:
        RLSpamOriginal=open(Input,encoding="utf-8").readlines()
    except BaseException:
        RLSpamOriginal=open(Input).readlines()
    FeatureList=LoadFeatureList(FeatureDir)
    RLSpam=[]
    for i in RLSpamOriginal:
        RLSpam.append(jieba.lcut(i,cut_all=False))

    try:
        for i in range(len(RLSpam)):
            for j in range(len(RLSpam[i])):
                RLSpam[i][j]=RLSpam[i][j].strip()
                RLSpam[i][j]=[RLSpam[i][j],0,0]
                for k in FeatureList:
                    if RLSpam[i][j][0]==k[0]:
                        RLSpam[i][j][1]=float(k[1])
                        RLSpam[i][j][2]=float(k[2])
    except BaseException:
        pass
    RRLSpam=[]
    for i in RLSpam[0]:
        if i[1]!=0:
            RRLSpam.append(i)
    while True:
        Modified=False
        for i in range(len(RRLSpam)-1):
            if RRLSpam[i][2]/RRLSpam[i][1]<RRLSpam[i+1][2]/RRLSpam[i+1][1]:
                Modified=True
                temp=RRLSpam[i]
                RRLSpam[i]=RRLSpam[i+1]
                RRLSpam[i+1]=temp
        if not Modified:
            break
    temp=[]
    RRRLSpam=[]
    fOut=open("Frequencies.txt","w",encoding="utf-8")
    for i in range(len(RRLSpam)):
        Duplicate=False
        for j in temp:
            if RRLSpam[i][0]==j:
                Duplicate=True
                break
        if Duplicate:
            continue
        temp.append(RRLSpam[i][0])
        fOut.write(RRLSpam[i][0]+" "+str(RRLSpam[i][1])+" "+str(RRLSpam[i][2])+" "+str(RRLSpam[i][2]/RRLSpam[i][1])+"\n")
        RRRLSpam.append(RRLSpam[i])
    fOut.close()

    SList=LoadSynonymList(SynonymDir)
    
    if Option==0:
        for i in RRRLSpam:
            if i[2]/i[1]>1:
                Change=False
                for j in SList:
                    ValList=[]
                    for k in j:
                        if k==i[0]:
                            for l in j:
                                ValList.append(Inquire(l,FeatureDir))
                            break
                    for k in range(len(ValList)):
                        if ValList[k]==min(ValList):
                            if ValList[k]<=0.7*i[2]/i[1]:
                                RLSpamOriginal[0]=RLSpamOriginal[0].replace(i[0],j[k])
                                Change=True
                if Change:
                    continue           
    else:
        for i in RRRLSpam:
            if i[2]/i[1]>1:        
                RLSpamOriginal[0]=RLSpamOriginal[0].replace(i[0],i[0][0]+" "+i[0][1:])
    fOut=open(Output,"w",encoding="utf-8")
    fOut.write(RLSpamOriginal[0])
    fOut.close()











def Classify(Input,FeatureDir,HamWordC,SpamWordC):
    print("Classifying Samples...")
    RLSpamOriginal=open(Input,encoding="utf-8").readlines()
    FeatureList=FeatureList=LoadFeatureList(FeatureDir)
    Vocab=[]
    for i in FeatureList:
        Vocab.append(i[0])
    RLSpam=[]
    for i in RLSpamOriginal:
        RLSpam.append(jieba.lcut(i,cut_all=False))

    def Cut2Vec(Sample,VocabList):
        Vec=zeros(len(VocabList))
        for i in range(len(VocabList)):
            for j in Sample:
                if j==VocabList[i]:
                    Vec[i]=1
        return Vec

    for i in range(len(RLSpam)):
        RLSpam[i]=Cut2Vec(RLSpam[i],Vocab)

    def Classification(Vec):
        LogHamPcd=0.0
        for j in range(len(Vec)):
            if Vec[j]==1:
                LogHamPcd+=math.log(float(FeatureList[j][1]))
        LogHamPcd+=math.log(HamWordC/(HamWordC+SpamWordC))        
        LogSpamPcd=0.0
        for j in range(len(Vec)):
            if Vec[j]==1:
                LogSpamPcd+=math.log(float(FeatureList[j][2]))
        LogSpamPcd+=math.log(SpamWordC/(HamWordC+SpamWordC))
        Addition=-(LogHamPcd+LogSpamPcd)/2
        LogHamPcd+=Addition
        LogSpamPcd+=Addition
        E1=0.3*math.e**LogSpamPcd
        E2=0.6*math.e**LogHamPcd
        g=E1-E2
        return g

    ReturnList=[]
    for i in RLSpam:
        ReturnList.append(Classification(i))
    
    return ReturnList










def Inquire(x,FeatureDir):
    FeatureList=open(FeatureDir,encoding="utf-8").readlines()
    try:
        for i in range(len(FeatureList)):
            FeatureList[i]=FeatureList[i].strip().split(" ")
            if len(FeatureList[i])!=3:
                del FeatureList[i]
    except BaseException:
        pass
    output=1
    for i in FeatureList:
        if i[0]==x:
            output=float(i[2])/float(i[1])
    return output










def LoadSynonymList(ListDir):
    f=open(ListDir,encoding="utf-8")
    SList=f.readlines()
    for i in range(len(SList)):
        SList[i]=SList[i].strip().split(" ")
    return SList









def PreprocessSynonym(SynonymDir,FeatureDir,Output1,Output2):
    fIn=open(SynonymDir)
    fOut=open(Output1,"w",encoding="utf-8")
    FeatureList=FeatureList=LoadFeatureList(FeatureDir)
    SList=fIn.readlines()
    for i in SList:
        if i.find("=")!=-1:
            fOut.write(i[i.find("=")+2:])
            continue
        if i.find("#")!=-1:
            fOut.write(i[i.find("#")+2:])
            continue
        if i.find("@")!=-1:
            fOut.write(i[i.find("@")+2:])
            continue
    fIn.close()
    fOut.close()
    
    def LoadSynonymList(ListDir):
        f=open(ListDir,encoding="utf-8")
        SList=f.readlines()
        for i in range(len(SList)):
            SList[i]=SList[i].strip().split(" ")
        return SList

    SList=LoadSynonymList(Output1)
    try:
        for j in range(len(SList)):
            Delete=True
            for i in FeatureList:
                for k in SList[j]:
                    if k==i[0]:
                        Delete=False
                        break
                if Delete==False:
                    break
            if Delete:
                del SList[j]
    except BaseException:
        pass
    fOut=open(Output2,"w",encoding="utf-8")
    for i in SList:
        temp=""
        for j in i:
            temp+=j+" "
        temp=temp[:len(temp)-1]+"\n"
        fOut.write(temp)
    fOut.close()
