module Fixture_call_ref_nested_in_list_Crystal_call
extend self
def process(data = nil); 0; end
my_var = 42
my_other = 7
process(data: [my_var, 42, "static"]);
process(data: [my_other, 7, "label"]);
end
