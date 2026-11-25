my $my_data = {
    'ancient_date' => Date.new(year => 1500, month => 3, day => 1),
    'modern_date' => Date.new(year => 2024, month => 1, day => 15),
    'before_date' => Date.new(year => 1582, month => 10, day => 4),
    'gap_date' => Date.new(year => 1582, month => 10, day => 10),
    'transition_date' => Date.new(year => 1582, month => 10, day => 15),
    'after_date' => Date.new(year => 1582, month => 10, day => 16),
    'before_naive' => DateTime.new(year => 1582, month => 10, day => 4, hour => 12, minute => 30, second => 0.000001, timezone => 0),
    'gap_naive' => DateTime.new(year => 1582, month => 10, day => 10, hour => 12, minute => 30, second => 0.5, timezone => 0),
    'transition_positive' => DateTime.new(year => 1582, month => 10, day => 14, hour => 6, minute => 30, second => 0, timezone => 0),
    'transition_negative' => DateTime.new(year => 1582, month => 10, day => 16, hour => 17, minute => 30, second => 0, timezone => 0),
    'after_positive' => DateTime.new(year => 1582, month => 10, day => 15, hour => 6, minute => 30, second => 0, timezone => 0),
};
