module Fixture_call_unknown_ref_nested_dict_Crystal_call
extend self
def process(data = nil); 0; end
my_list = [] of Nil
process(data: [[{"inner" => my_list}]]);
end
