module Fixture_call_ref_args_heterogeneous_list_Crystal_call
extend self
def process(data = nil, count = nil); 0; end
my_ints = [
    1,
    2,
    3,
]
my_strings = [
    "a",
    "b",
]
my_empty = [] of Nil
process(data: my_ints, count: 42);
process(data: my_strings, count: 7);
process(data: my_empty, count: 99);
end
