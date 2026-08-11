use JSON::PP;
my $my_data = [
    {"id" => 100, "label" => "first entry", "enabled" => JSON::PP::false, "related_ids" => [102, 103]},
    {"id" => 101, "label" => "second entry", "enabled" => JSON::PP::true, "related_ids" => [100]},
];
$my_data = [
    {"id" => 100, "label" => "first entry", "enabled" => JSON::PP::false, "related_ids" => [102, 103]},
    {"id" => 101, "label" => "second entry", "enabled" => JSON::PP::true, "related_ids" => [100]},
];
