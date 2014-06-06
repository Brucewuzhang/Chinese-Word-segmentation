#!/usr/bin/env python
#coding:utf-8

import codecs,re


class Process(object):
    def __init__(self,file_dir,S):
        self._file_dir = file_dir
        self._S = S
    
    '''
    def _read(self):
        f = open(self._file_dir,'rb')
        regex=re.compile("(?x) ( [\w-]+ | [\x80-\xff]{3} )")
        train = []
        for line in f.readlines():
            line = line.replace(' ','')
            line = line.replace('\r\n','')
            words = [w for w in regex.split(line) if w]
            if len(words) != 0:
                train.append(words)
        return train
    '''

    def _str2words(self,string):
        words =[]
        regex=re.compile("(?x) ( [\w-]+ | [\x80-\xff]{3} )")
        words = [w for w in regex.split(string) if w]
        return words
    def _statics_hidden(self):
        '''
        First,get the tokenize result of the corpus,
        statics the hidden state of each word
        '''
        f = open(self._file_dir,'rb')
        hidden_states,train = [],[]
        regex=re.compile("(?x) ( [\w-]+ | [\x80-\xff]{3} )")
        for line in f.readlines():
            hidden_state = ''
            words = []
            tokenizes = line.split()
            for token in tokenizes:
                temp = [w for w in regex.split(token) if w]
                for t in temp:
                    words.append(t)
                length = len(temp)
                if length == 1:
                    hidden_state += 'S'
                elif length==2:
                    hidden_state += 'BE'
                else:
                    hidden_state += 'B'+(length-2)*'M'+'E'
            if len(words) != 0:
                train.append(words)
                hidden_states.append(hidden_state)
        return (hidden_states,train)

    def _word_count(self,train):
        word_count = {}
        for words in train:
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
        return word_count
    
    def _convert(self,hidden_states):
        temp = []
        for index in range(len(hidden_states)):
            regex = re.compile("(\w{1})")
            states = [w for w in regex.split(hidden_states[index]) if w]
            if len(states) !=0:
                temp.append(states)
        return temp
    
    def _cal_trans(self,h_s):
        trans_prob,state_count = {},{}
        #intial
        for state in self._S:
            trans_prob[state]={}
            state_count[state] = 0
            for state_i in self._S:
                trans_prob[state][state_i]=0
        for i in range(len(h_s)):
            length = len(h_s[i])
            for j in range(length-1):
                s_from = h_s[i][j]
                s_to = h_s[i][j+1]
                trans_prob[s_from][s_to] += 1
                state_count[s_from] += 1
            state_count[h_s[i][length-1]] += 1
        print state_count
        for i in self._S:
            for j in self._S:
                trans_prob[i][j] /= float(state_count[i])
        print trans_prob
        return (trans_prob,state_count)
    
    def _cal_conf(self,h_s,word_count,train,state_count):
        conf_prob = {}
        words = word_count.keys()
        print('The corpus has %d word'%(len(words)))
        for state in self._S:
            conf_prob[state] = {}
            for word in words:
                conf_prob[state][word] = 0
        for i in range(len(h_s)):
            length = len(h_s[i])
            for j in range(length):
                obser = train[i][j]
                hidden = h_s[i][j]
                conf_prob[hidden][obser] += 1
        for state in self._S:
            for word in words:
                if conf_prob[state][word] == 0:
                    continue
                else:
                    conf_prob[state][word] /= float(state_count[state])
        return conf_prob
        

    def _tran_conf_prob(self,train,word_count,hidden_states):
        #convert the hidden_state string to list
        hidden_states = self._convert(hidden_states)
        trans_prob,state_count = self._cal_trans(hidden_states)
        conf_prob = self._cal_conf(hidden_states,word_count,train,state_count)
        
        return (conf_prob,trans_prob)
        


        

