use DateTime;
my $my_data = [
    1,
    1.5,
    undef,
    DateTime->new(year => 2020, month => 1, day => 1),
    DateTime->new(year => 2020, month => 1, day => 1, hour => 0, minute => 0, second => 0, time_zone => 'UTC'),
    [],
];
