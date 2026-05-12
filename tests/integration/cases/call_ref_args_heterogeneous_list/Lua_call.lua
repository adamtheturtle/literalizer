function process(...) end
local my_ints = {
    1,
    2,
    3,
}
local my_strings = {
    "a",
    "b",
}
local my_empty = {}
process(my_ints, 42)
process(my_strings, 7)
process(my_empty, 99)
