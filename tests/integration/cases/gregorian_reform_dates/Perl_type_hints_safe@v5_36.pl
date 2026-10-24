use DateTime;
my $my_data = {
    "before_date" => DateTime->new(year => 1582, month => 10, day => 4),
    "gap_date" => DateTime->new(year => 1582, month => 10, day => 10),
    "transition_date" => DateTime->new(year => 1582, month => 10, day => 15),
    "after_date" => DateTime->new(year => 1582, month => 10, day => 16),
    "before_naive" => DateTime->new(year => 1582, month => 10, day => 4, hour => 12, minute => 30, second => 0, nanosecond => 1000, time_zone => 'UTC'),
    "gap_naive" => DateTime->new(year => 1582, month => 10, day => 10, hour => 12, minute => 30, second => 0, nanosecond => 500000000, time_zone => 'UTC'),
    "transition_positive" => DateTime->new(year => 1582, month => 10, day => 14, hour => 6, minute => 30, second => 0, time_zone => 'UTC'),
    "transition_negative" => DateTime->new(year => 1582, month => 10, day => 16, hour => 17, minute => 30, second => 0, time_zone => 'UTC'),
    "after_positive" => DateTime->new(year => 1582, month => 10, day => 15, hour => 6, minute => 30, second => 0, time_zone => 'UTC'),
};
