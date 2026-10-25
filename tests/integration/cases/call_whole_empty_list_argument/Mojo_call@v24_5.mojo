def f[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    f(List[String]())
