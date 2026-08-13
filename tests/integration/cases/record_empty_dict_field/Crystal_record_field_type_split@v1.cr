module Fixture_record_empty_dict_field_Crystal_record_field_type_split
extend self
record Record0, f : Hash(String, String), g : Int32
my_data = Record0.new(
    {} of String => String,
    1,
)
end
