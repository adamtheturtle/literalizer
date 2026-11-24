class F_ {
    construct new() {}
    call(a, b) {}
}
var f = F_.new()
// calls heading
// before call one
// first argument
f.call(1, 2)  // after call one
// second argument
f.call(3, 4)
// after all calls
