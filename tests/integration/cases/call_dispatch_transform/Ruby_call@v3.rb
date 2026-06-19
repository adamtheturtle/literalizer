def record_value(*a); end
def flush_buffer(*a); end
def emit(*a); end
emit(record_value(value: 42))
flush_buffer(count: 3)
