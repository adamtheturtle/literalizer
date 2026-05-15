use DateTime;
my $my_data = {
    "within_i32" => DateTime->new(year => 2024, month => 1, day => 15, hour => 12, minute => 0, second => 0, time_zone => 'UTC'),
    "beyond_i32" => DateTime->new(year => 2099, month => 6, day => 15, hour => 8, minute => 30, second => 0, time_zone => 'UTC'),
};
$my_data = {
    "within_i32" => DateTime->new(year => 2024, month => 1, day => 15, hour => 12, minute => 0, second => 0, time_zone => 'UTC'),
    "beyond_i32" => DateTime->new(year => 2099, month => 6, day => 15, hour => 8, minute => 30, second => 0, time_zone => 'UTC'),
};
