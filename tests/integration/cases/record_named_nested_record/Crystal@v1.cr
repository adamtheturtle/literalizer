module Fixture_record_named_nested_record_Crystal
extend self
my_data = {
    "project" => "alpha",
    "lead_item" => {"id" => 100, "label" => "first item", "enabled" => false, "related_ids" => [102, 103]},
}
end
