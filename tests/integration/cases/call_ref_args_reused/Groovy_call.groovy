def process(Map _args) { null }
def shared = 1
def other = 2
process(data: shared, count: 1)
process(data: other, count: 0)
process(data: shared, count: 8)
