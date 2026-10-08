my_data = struct(
    'cr', sprintf('%s%s%s', "a", char(13), "b"),
    'crlf', sprintf('%s%s%s%s', "a", char(13), char(10), "b"),
    'lf', sprintf('%s%s%s', "a", char(10), "b")
);
