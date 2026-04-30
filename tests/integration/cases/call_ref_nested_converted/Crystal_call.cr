module Fixture_call_ref_nested_converted_Crystal_call
extend self
def process(data = nil); 0; end
my_var = 42
process(data: [{"ref" => "myVar"}, 42, "static"]);
end
