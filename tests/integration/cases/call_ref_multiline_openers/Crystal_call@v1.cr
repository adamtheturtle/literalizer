module Fixture_call_ref_multiline_openers_Crystal_call
extend self
def consume(items = nil, mapping = nil); 0; end
foo = 42
consume(items: [
    {
        "other" => 1,
    },
    foo,
], mapping: {
    "left" => foo,
    "other" => 1,
});
end
