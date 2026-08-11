my_data = {
    sprintf('%s%s%s%s%s%s%s', "C:", char(92), "path", char(92), "to", char(92), "file"),
    sprintf('%s%s%s%s', "back", char(92), char(92), "slash"),
    sprintf('%s%s%s%s%s', "hello ", char(92), """world", char(92), """"),
    sprintf('%s%s%s', "path", char(92), "to ""# file"),
    sprintf('%s%s', "trailing", char(92)),
    "both ""quotes''' here",
    sprintf('%s%s%s%s%s', "line1", char(92), "nline2", char(10), "with newline")
};
