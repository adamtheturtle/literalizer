module Fixture_call_ref_nested_reusable_Crystal_sequence_tuple_call
extend self
def process(data = nil); 0; end
item = {
    1,
    2,
}
process(data: {item, item});
end
