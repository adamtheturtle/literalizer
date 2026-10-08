my $my_data = {
    "double" => "a\x{2028}b",
    "single" => "c\x{2029}d",
    "both" => "e\x{2028}f\x{2029}g",
    "continued" => "hi",
    "escaped backslash" => "j\\\x{2028}k",
};
