def process(*a); end
def emit(*a); end
emit(process(value: 1), Time.utc(2024, 1, 15, 12, 0, 0))
