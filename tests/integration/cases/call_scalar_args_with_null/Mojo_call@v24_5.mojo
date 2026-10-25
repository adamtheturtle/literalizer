def process[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    process(None)
    process("hello")
