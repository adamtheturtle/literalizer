module Fixture_dict_colliding_cobol_keys_Crystal_combined
extend self
my_data = {
    "user_name" => 1,
    "user.name" => 2,
    "user-name" => 3,
    "field_name_that_is_really_quite_long_one" => 4,
    "field_name_that_is_really_quite_long_two" => 5,
}
my_data = {
    "user_name" => 1,
    "user.name" => 2,
    "user-name" => 3,
    "field_name_that_is_really_quite_long_one" => 4,
    "field_name_that_is_really_quite_long_two" => 5,
}
end
