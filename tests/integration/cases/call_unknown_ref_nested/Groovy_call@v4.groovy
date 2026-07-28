def process(Map _args) { null }
def known_value = true
def unknown_value = true
process(known_value: known_value, nested_missing: [unknown_value])
