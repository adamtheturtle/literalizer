use DateTime;
my $my_data = {
    "ancient_date" => DateTime->new(year => 1500, month => 3, day => 1),
    "modern_date" => DateTime->new(year => 2024, month => 1, day => 15),
    "before_date" => DateTime->new(year => 1582, month => 10, day => 4),
    "gap_date" => DateTime->new(year => 1582, month => 10, day => 10),
    "transition_date" => DateTime->new(year => 1582, month => 10, day => 15),
    "after_date" => DateTime->new(year => 1582, month => 10, day => 16),
    "before_naive" => "1582-10-04T12:30:00.000001",
    "gap_naive" => "1582-10-10T12:30:00.500000",
    "transition_positive" => "1582-10-15T00:30:00+18:00",
    "transition_negative" => "1582-10-15T23:30:00-18:00",
    "after_positive" => "1582-10-16T00:30:00+18:00",
};
