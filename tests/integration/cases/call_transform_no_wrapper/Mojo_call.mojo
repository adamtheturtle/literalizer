fn process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    process("hello")
    process(42)
    process(True)
