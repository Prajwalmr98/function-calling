from methods import add_method,mul_method
def test_add_method():
    assert add_method(3,6)==9
    assert add_method(1, -4) == -3
def test_mul_method():
    assert mul_method(-3,6)==-18
    assert mul_method(2, 3) == 6
def main_method():
    add_res,mul_res=main_method(3,6)
    assert  add_res==9
    assert mul_res==18