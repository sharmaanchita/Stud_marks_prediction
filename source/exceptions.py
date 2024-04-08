import sys
from source.logger import logging

def error_message(error,error_detail:sys):
    _,_,exc_tb = error_detail.exec_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_print = "Error occured in script name[{0}] line number [{1}] error message".format(file_name,exc_tb.tb_lineno,str(error))
    return error_print

class CustomException(Exception):
    def __init__(self,error_print,error_detail:sys):
        super().__init__(error_print)
        self.error_print = error_message(error_print,error_detail=error_detail)
    def __str__(self):
        return self.error_print
    