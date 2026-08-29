function process(...) end
local big_list = {
    "x",
}
process({["k"] = big_list}, {["m"] = big_list})
