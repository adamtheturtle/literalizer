class F_ {
    construct new() {}
    call(ops) {}
}
var f = F_.new()
f.call([["DEL", "b", "10"], ["ADD", "a", "x"]])  // note
// next call
f.call([["ADD", "c", "y"]])
