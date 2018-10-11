# -*- coding: UTF-8 -*-
"""
check the security and functionability of uploaded code 
- forbid from importing os
- random chessboard check
- some special case check
"""
import imp
import traceback

import numpy as np
import time

FORBIDDEN_LIST = ['import os', 'exec']

class CodeCheck():
    def __init__ (self, script_file_path, chessboard_size):
        self.time_out = 5
        self.script_file_path = script_file_path
        self.chessboard_size = chessboard_size
        self.agent = None
        self.errormsg = 'Error'
        # print(self.chessboard)

    # Call this function and get True or False, self.errormsg has the massage
    def check_code(self):
        # check if contains forbidden library
        if self.__check_forbidden_import() == False:
            return False
    
        # check initialization
        try:
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)
        except Exception:
            self.errormsg = "Fail to init"
            return False
    
        # check simple condition
        if not self.__check_simple_chessboard():
            self.errormsg = "Can not pass usability test."
            return False
    
        # check advance condition, online test contain more test case than this demo
        if not self.__check_advance_chessboard():
            self.errormsg = "Your code is too weak, fail to pass base test."
            return False

        return True


    def __check_forbidden_import(self):
        with open(self.script_file_path, 'r', encoding='UTF-8') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True
    
    def __check_go (self, chessboard):
        self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)
        try:
            self.agent.go(np.copy(chessboard))
        except Exception:
            self.errormsg = "Error:" + traceback.format_exc()
            return False
        return True
    
    def __check_result (self, chessboard, result):
        if not self.__check_go(chessboard):
            return False
        if not self.agent.candidate_list or list(self.agent.candidate_list[-1]) not in result:
            return False
        return True
        
    def __check_simple_chessboard(self):
        # empty chessboard
        if not self.__check_go(np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)):
            return False
    
        # only one empty position remain
        chessboard = np.ones((self.chessboard_size, self.chessboard_size))
        chessboard[:, ::2] = -1
        for i in range(0, self.chessboard_size, 4):
            chessboard[i] = -chessboard[i]
        x, y = np.random.choice(self.chessboard_size, 2)
        chessboard[x, y] = 0
    
        if not self.__check_result(chessboard, [[x, y]]):
            return False

        return True
    
    def __check_advance_chessboard (self):
        # win
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:4] = -1
        chessboard[1, 0:4] = 1
        if not self.__check_result(chessboard, [[0, 4]]):
            return False
    
        # defense 5 inline
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:2] = -1
        chessboard[0, 7] = -1
        chessboard[1, 1:4] = 1
        if not self.__check_result(chessboard, [[1, 4], [1, 0]]):
            return False
    
        # two three
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[1, 1:3] = -1
        chessboard[2:4, 3] = -1
        chessboard[1, 6:8] = 1
        chessboard[2:4, 8] = 1
        if not self.__check_result(chessboard, [[1, 3]]):
            return False
    
        # defense
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:2] = -1
        chessboard[0:2, self.chessboard_size-1] = -1
        chessboard[1, 6:8] = 1
        chessboard[2:4, 8] = 1
        if not self.__check_result(chessboard, [[0, 8], [1, 8], [4, 8], [5, 8], [1, 5], [1, 9], [1, 10]]):
            return False

        return True
