sub capture(*@a, *%kw) {}
capture(NaN, Inf, -Inf, 1.250000e0, Date.new(year => 2024, month => 1, day => 15), DateTime.new(year => 2024, month => 1, day => 15, hour => 12, minute => 34, second => 56, timezone => 0), '[ordinary text]');
