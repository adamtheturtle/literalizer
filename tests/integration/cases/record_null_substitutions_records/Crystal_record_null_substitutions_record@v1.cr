module Fixture_record_null_substitutions_records_Crystal_record_null_substitutions_record
extend self
record Record0, due_date : Int32, parent_id : Int32, assignee : String
my_data = [
    Record0.new(-1, -1, ""),
    Record0.new(10, 20, "alice"),
]
end
