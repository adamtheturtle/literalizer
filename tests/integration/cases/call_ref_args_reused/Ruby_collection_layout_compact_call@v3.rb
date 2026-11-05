def process(*a); end
single_var = [
  4,
  5,
  6,
]
repeated_var = 1
process(data: repeated_var, count: 1)
process(data: single_var, count: 0)
process(data: repeated_var, count: 8)
