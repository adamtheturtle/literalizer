def process(*a); end
def emit(*a); end
emit(process(value: "hello"), true)
emit(process(value: 42), false)
