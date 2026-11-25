use DateTime;
my $my_data = {
    "half" => DateTime->new(year => 1979, month => 5, day => 27, hour => 7, minute => 32, second => 0, nanosecond => 500000000, time_zone => 'UTC'),
    "milli" => DateTime->new(year => 1979, month => 5, day => 27, hour => 7, minute => 32, second => 0, nanosecond => 100000000, time_zone => 'UTC'),
    "max_milli" => DateTime->new(year => 1979, month => 5, day => 27, hour => 7, minute => 32, second => 0, nanosecond => 999000000, time_zone => 'UTC'),
    "whole" => DateTime->new(year => 1979, month => 5, day => 27, hour => 7, minute => 32, second => 0, time_zone => 'UTC'),
};
