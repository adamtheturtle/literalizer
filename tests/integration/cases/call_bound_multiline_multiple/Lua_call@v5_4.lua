function f(...) end
local ref_data = {
    1,
    2,
}
f({
    ref_data,
})
f({
    ref_data,
})
