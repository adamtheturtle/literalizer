my $my_data = {
    'before_date' => "1582-10-04",
    'gap_date' => "1582-10-10",
    'transition_date' => "1582-10-15",
    'after_date' => "1582-10-16",
    'before_naive' => DateTime.new(year => 1582, month => 10, day => 4, hour => 12, minute => 30, second => 0.000001, timezone => 0),
    'gap_naive' => DateTime.new(year => 1582, month => 10, day => 10, hour => 12, minute => 30, second => 0.5, timezone => 0),
    'transition_positive' => DateTime.new(year => 1582, month => 10, day => 14, hour => 6, minute => 30, second => 0, timezone => 0),
    'transition_negative' => DateTime.new(year => 1582, month => 10, day => 16, hour => 17, minute => 30, second => 0, timezone => 0),
    'after_positive' => DateTime.new(year => 1582, month => 10, day => 15, hour => 6, minute => 30, second => 0, timezone => 0),
};
