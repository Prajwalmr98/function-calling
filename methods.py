def add_method (a,b):
    return a+b
def mul_method( a,b):
    return a*b
def main_method(a,b):
    add_res=add_method(a,b)
    mul_res=mul_method(a,b)
    print(f"sum of {a} and {b} is:{add_res}")
    print(f"mul of {a} and {b} is:{mul_res}")

main_method(2,3)