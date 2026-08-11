local foo = {
    ["_"] = "_",
}
local my_data = {
    ["mapping"] = {["value"] = foo},
    ["items"] = {{["other"] = 1}, foo},
}
