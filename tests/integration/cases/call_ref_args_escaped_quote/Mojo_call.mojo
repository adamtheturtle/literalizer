fn process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    var my_str = "a\"b"
    process(my_str^)
