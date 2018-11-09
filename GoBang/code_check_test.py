#!/usr/bin/env python3
import sys
from code_check import CodeCheck
from code_check1 import CodeCheck as cc1
from code_check2 import CodeCheck as cc2
from code_check3 import CodeCheck as cc3

def main():
    code_checker = CodeCheck("Go.py", 15)
    code_checker1 = cc1("Go.py", 15)
    code_checker2 = cc2("Go.py", 15)
    code_checker3 = cc3("Go.py", 15)
    if not code_checker.check_code():
        print("not pass")
        print(code_checker.errormsg)
    else:
        print('pass')

    if not code_checker1.check_code():
        print("not pass")
        print(code_checker.errormsg)
    else:
        print('pass')

    if not code_checker2.check_code():
        print("not pass")
        print(code_checker.errormsg)
    else:
        print('pass')

    if not code_checker3.check_code():
        print("not pass")
        print(code_checker.errormsg)
    else:
        print('pass')


if __name__ == '__main__':
    print("a")
    main()

