def record_value(Map _args) { null }
def flush_buffer(Map _args) { null }
def emit(Map _args) { null }
emit(record_value(value: 42))
flush_buffer(count: 3)
