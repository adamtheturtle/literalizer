module Fixture_dict_colliding_normalized_long_keys_Crystal
extend self
my_data = {
    "a_b" => 1,
    "a-b" => 2,
    "averyveryverylongkeynamethatgoesonandonandon" => 3,
    "averyveryverylongkeynamethatgoesonandmore" => 4,
}
end
