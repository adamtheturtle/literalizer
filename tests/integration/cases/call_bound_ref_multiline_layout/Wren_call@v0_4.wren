class F_ {
    construct new() {}
    call(value) {}
}
var f = F_.new()
var ref_data = [
    [
        1,
        2,
    ],
    [
        3,
        4,
    ],
]
f.call([
    [
        ref_data,
    ],
])
