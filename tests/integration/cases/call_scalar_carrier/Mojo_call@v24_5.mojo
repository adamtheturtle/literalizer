def process[*Ts: AnyType](var *args: *Ts):
    pass
def main():
    process("hello")
    process(42)
    process(True)
    process(None)
