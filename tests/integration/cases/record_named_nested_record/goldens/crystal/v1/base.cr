module Fixture_record_named_nested_record_Crystal
extend self
my_data = {
    "collection" => "alpha",
    "featured_entry" => {"id" => 100, "label" => "first entry", "enabled" => false, "related_ids" => [102, 103]},
}
end
