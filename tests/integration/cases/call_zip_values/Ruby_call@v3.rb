def process(*a); end
def emit(*a); end
emit(process(value: "hello"), 1)
emit(process(value: 42), 0)
