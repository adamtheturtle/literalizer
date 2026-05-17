module Fixture_record_nested_container_Crystal_heterogeneous_strategy_record
extend self
record Record0, title : String, tags : Array(String), priority : Int32
my_data = Record0.new(
    "report",
    [
        "draft",
        "urgent",
        "review",
    ],
    2,
)
end
