def process(*a); end
known_value = true
unknown_value = true
process(known_value: known_value, nested_missing: [unknown_value])
