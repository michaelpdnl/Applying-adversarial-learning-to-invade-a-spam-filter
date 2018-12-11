import SpamFilter

if __name__!="__main__":
    Arrange("ham_all.txt","HamTrain.txt",range(3000))
    Arrange("ham_all.txt","HamTest.txt",range(3000,3200))
    Arrange("spam_all.txt","SpamTrain.txt",range(3000))
    Arrange("spam_all.txt","SpamTest.txt",range(3000,3200))
    H,S=Train("HamTrain.txt","SpamTrain.txt","Features.txt")
    print(Classify("SpamTest.txt","Features.txt",H,S))
