module Fixture_record_nested_map_fallback_Crystal_record_nested_map_fallback_multiline
extend self
alias LiteralizerRecordValue = Bool | Float64 | Int128 | Int32 | Int64 | String | Nil
record Record0, name : String, input : Hash(String, LiteralizerRecordValue), expected : Hash(String, LiteralizerRecordValue)
my_data = [
    Record0.new(
        "test_1",
        Hash(String, LiteralizerRecordValue){
            "type" => "create",
            "pr_id" => "pr_1",
            "draft" => true,
            "missing" => nil,
        },
        Hash(String, LiteralizerRecordValue){
            "pr_id" => "pr_1",
            "status" => "draft",
        },
    ),
    Record0.new(
        "test_2",
        Hash(String, LiteralizerRecordValue){
            "type" => "publish",
            "pr_id" => "pr_1",
        },
        Hash(String, LiteralizerRecordValue){
            "error" => "invalid_operation",
        },
    ),
]
end
