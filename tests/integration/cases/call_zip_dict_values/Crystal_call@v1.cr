module Fixture_call_zip_dict_values_Crystal_call
extend self
def process(value = nil); 0; end
def emit(_call = nil, _zip = nil); 0; end
emit(process(value: "hello"), {"a" => 1, "b" => 2});
emit(process(value: 42), {"c" => 3, "d" => 4});
end
