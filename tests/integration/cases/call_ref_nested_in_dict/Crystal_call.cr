module Fixture_call_ref_nested_in_dict_Crystal_call
extend self
def process(data = nil); 0; end
my_var = 42
process(data: {"key" => {"ref" => "my_var"}, "count" => 42});
end
