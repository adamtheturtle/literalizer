def f[*Ts: Movable](var *args: *Ts):
    pass
def main():
    f(List[String]())
