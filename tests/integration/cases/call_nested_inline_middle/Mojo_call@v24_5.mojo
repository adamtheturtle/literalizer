def f(ops: List[List[String]]):
    pass
def main():
    f(List([List(["DEL", "b", "10"]), List(["ADD", "a", "x"])]))  # note
    # next call
    f(List([List(["ADD", "c", "y"])]))
