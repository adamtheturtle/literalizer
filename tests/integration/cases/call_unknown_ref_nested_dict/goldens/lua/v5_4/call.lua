function process(...) end
local my_list = {
    ["unused"] = "value",
}
process({{{["inner"] = my_list}}})
