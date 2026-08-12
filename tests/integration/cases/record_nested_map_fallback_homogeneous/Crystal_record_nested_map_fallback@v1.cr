module Fixture_record_nested_map_fallback_homogeneous_Crystal_record_nested_map_fallback
extend self
alias LiteralizerRecordValue = Bool | Float64 | Int128 | Int32 | Int64 | String | Nil
record Record1, kind : String, pr_id : String
record Record0, name : String, input : Record1, expected : Hash(String, LiteralizerRecordValue)
my_data = [
    Record0.new("test_1", Record1.new("create", "pr_1"), Hash(String, LiteralizerRecordValue){"pr_id" => "pr_1", "status" => "draft"}),
    Record0.new("test_2", Record1.new("publish", "pr_1"), Hash(String, LiteralizerRecordValue){"error" => "invalid_operation"}),
]
end
