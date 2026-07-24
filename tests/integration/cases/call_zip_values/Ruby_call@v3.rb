def process(*a); end
def emit(*a); end
emit(process(value: "hello"), "one")
emit(process(value: 42), "zero")
