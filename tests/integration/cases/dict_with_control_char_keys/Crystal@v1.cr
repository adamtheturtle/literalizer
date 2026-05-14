module Fixture_dict_with_control_char_keys_Crystal
extend self
my_data = {
    "key\nwith\nnewlines" => "value1",
    "key\twith\ttabs" => "value2",
    "" => "value3",
}
end
