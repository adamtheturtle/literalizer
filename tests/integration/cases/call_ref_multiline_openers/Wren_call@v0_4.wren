class Consume_ {
    construct new() {}
    call(items, mapping) {}
}
var consume = Consume_.new()
var foo = 42
consume.call([
    {
        "other": 1,
    },
    foo,
], {
    "left": foo,
    "other": 1,
})
