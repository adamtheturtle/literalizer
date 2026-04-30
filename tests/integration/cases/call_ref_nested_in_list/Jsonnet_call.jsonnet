local my_var = 42;
local my_other = 7;
local process(data) = null;
[
    process(data=[{ref: "my_var"}, 42, "static"]),
    process(data=[{ref: "my_other"}, 7, "label"]),
]
