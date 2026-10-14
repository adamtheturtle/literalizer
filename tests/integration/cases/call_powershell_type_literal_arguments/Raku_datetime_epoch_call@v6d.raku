sub capture(*@a, *%kw) {}
capture(NaN, Inf, -Inf, 1.25e0, Date.new(year => 2024, month => 1, day => 15), 1705322096, '[ordinary text]');
