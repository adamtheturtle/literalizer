function consume(...) end
local foo = 42
consume({
    {
        ["other"] = 1,
    },
    foo,
}, {
    ["left"] = foo,
    ["other"] = 1,
})
