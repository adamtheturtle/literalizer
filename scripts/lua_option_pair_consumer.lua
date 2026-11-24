local json = require "dkjson"
local value = dofile("option_data.lua")

assert(math.type(value.count) == "integer", "expected integer count")
assert(math.type(value.nested[1]) == "integer", "expected nested integer")
io.write(json.encode(value))
