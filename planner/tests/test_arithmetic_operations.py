def add(a:int, b:int)->int:
    return a+b
def subtract(a:int, b:int)->int:
    return b-a
def multiply(a:int, b:int)->int:
    return a*b

# ----------- [test] --------------- #

def test_add()->None:
    assert add(1,1)==2

def test_subtract()->None:
    assert subtract(9,8)==-1

def test_multiply()->None:
    assert multiply(9,8)==72