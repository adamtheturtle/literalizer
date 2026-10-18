use DateTime;
my $my_data = [
    DateTime->new(year => 1970, month => 1, day => 1, hour => 0, minute => 0, second => 0, nanosecond => 1000, time_zone => 'UTC'),
    DateTime->new(year => 1969, month => 12, day => 31, hour => 23, minute => 59, second => 59, nanosecond => 500000000, time_zone => 'UTC'),
    DateTime->new(year => 1970, month => 1, day => 1, hour => 0, minute => 0, second => 1, time_zone => 'UTC'),
];
