my_data = {
    % strings stay data
    "https://example.org/a/*b*/",  % URL annotation
    "escaped quote: "" // still data",
    sprintf('%s%s', "backslash: ", char(92)),  % outside the string
    "/* not a comment */"
};
