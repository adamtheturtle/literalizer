use DateTime;
my $my_data = {
    "date" => DateTime->new(year => 99, month => 5, day => 27),
    "naive" => DateTime->new(year => 1, month => 1, day => 1, hour => 12, minute => 30, second => 0, time_zone => 'UTC'),
    "recent" => DateTime->new(year => 2024, month => 5, day => 27, hour => 10, minute => 0, second => 0, time_zone => 'UTC'),
};
