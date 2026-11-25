def process[*Ts: Movable](var *args: *Ts):
    pass
def main():
    process(None)
    process(List([1, 2]))
