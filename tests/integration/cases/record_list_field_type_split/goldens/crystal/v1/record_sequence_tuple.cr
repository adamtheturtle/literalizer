module Fixture_record_list_field_type_split_Crystal_record_sequence_tuple
extend self
record Record1, kind : String, urgent : Bool
record Record0, entries : Tuple(Record1)
record Record3, error : String
record Record2, entries : Tuple(Record3)
my_data = {
    "left" => Record0.new({Record1.new("add", true)}),
    "right" => Record2.new({Record3.new("not_found")}),
}
end
