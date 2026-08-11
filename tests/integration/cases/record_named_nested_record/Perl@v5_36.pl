use JSON::PP;
my $my_data = {
    "collection" => "alpha",
    "featured_entry" => {"id" => 100, "label" => "first entry", "enabled" => JSON::PP::false, "related_ids" => [102, 103]},
};
