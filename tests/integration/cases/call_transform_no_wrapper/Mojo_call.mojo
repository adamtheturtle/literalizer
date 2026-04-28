def main():
    def process(*args: object) -> object: return object()
    process("hello")
    process(42)
    process(True)
