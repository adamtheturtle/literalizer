def process(Map _args) { null }
def emit(Map _args) { null }
emit(process(value: "hello"), true)
emit(process(value: 42), false)
