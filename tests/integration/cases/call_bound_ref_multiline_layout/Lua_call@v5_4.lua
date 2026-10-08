function f(...) end
local x = {
    {
        1,
        2,
    },
    {
        3,
        4,
    },
}
f({
    {
        x,
    },
})
