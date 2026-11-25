use DateTime;
sub check {}
check(DateTime->new(year => 2024, month => 1, day => 15, hour => 10, minute => 30, second => 0, time_zone => 'UTC'), DateTime->new(year => 2024, month => 6, day => 1));
