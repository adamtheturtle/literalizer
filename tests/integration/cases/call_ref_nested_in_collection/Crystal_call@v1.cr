module Fixture_call_ref_nested_in_collection_Crystal_call
extend self
def process(a = nil, b = nil); 0; end
big_list = [
    "x",
]
process(a: {"k" => big_list}, b: 2);
end
