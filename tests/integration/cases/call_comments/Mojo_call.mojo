fn process[*Ts: AnyType](*args: *Ts):
    pass
def main():
    # Test cases
    process("hello")  # single word
    process("hello world")  # two words
    # trailing comment
