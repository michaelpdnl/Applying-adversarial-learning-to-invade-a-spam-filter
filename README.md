# Applying-adversarial-learning-to-invade-a-spam-filter
The author of the code is Yuanhao Luo from Shanghai Experimental School. 
This piece of code is for the GSF project "Applying adversarial learning to invade a spam filter".
Email of the author: michaelpdnl@163.com
Wechat account of the author: michaelpdnl


The spam filter operated successfully in the environment of Python 3.5.4 (64 bit).
To run the code, please ensure that you have installed numpy and jieba.
Installation method: open the cmd and type "pip install numpy" and "pip install jieba".


In all .txt files, a line represents a sample.

ham_all.txt: all hams in the database
spam_all.txt: all spams in the database
Synonym.txt: the Harbin Institute of Technology Extended Synonym corpus
AttackPoint0.txt: initial attack point


To use the following methods, please add "import SpamFilter" to the beginning of your code.
To see examples, open UserExample.py.
Should there be any questions, please contact the author. 

Methods and their usage:
Train(HamDir,SpamDir,Output) return HamWordC,SpamWordC
	HamDir: the ham part of the emails
	SpamDir: the spam part of the emails
	Output: the output directory of the vocabulary list
	HamWordC: the total word count of hams
	SpamWordC: the total word count of spams

Arrange(Input,Output,Range)
	Input: directory of the dataset
	Output: output directory
	Range: range of extraction

Classify(Input,FeatureDir,HamWordC,SpamWordC) return ReturnList
	Input: the testing set
	FeatureDir: the directory of the vocabulary list
	HamWordC: the total word count of hams
	SpamWordC: the total word count of spams
	ReturnList: result of the continuous classification function (+1 means spam and -1 means ham)

Iterate(Input,Output,SynonymDir,FeatureDir,Option)
	Input: directory of the initial attack point
	Output: directory of the improved attack point
	SynonymDir: synonym corpus that has undergone preprocessing
	FeatureDir: the directory of the vocabulary list
	Option: the mode of attack (=0 means step 1, =1 means step 2)

Inquire(x,FeatureDir) return output
	x: the word inquired
	FeatureDir: the directory of the vocabulary list
	output: the phi value of the word

PreprocessSynonym(SynonymDir,FeatureDir,Output1,Output2)
	SynonymDir: the original synonym directory
	FeatureDir: the directory of the vocabulary list
	Output1: the preprocessed synonym list
	Output2: the preprocessed and truncated synonym list
