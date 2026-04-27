module Check
extend self
def process(data = nil, count = nil); 0; end
my_var = [
    1,
    2,
    3,
]
my_other = [
    4,
    5,
    6,
]
process(data: my_var, count: 42);
process(data: my_other, count: 7);
end
