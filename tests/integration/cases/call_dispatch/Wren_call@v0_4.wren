class Put_ {
    construct new() {}
    call(key, value) {}
}
var put = Put_.new()
class Get_ {
    call(key) {}
var get = Get_.new()
put.call(1, 10)
get.call(1)
