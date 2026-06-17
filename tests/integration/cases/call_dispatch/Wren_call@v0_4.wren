class Store_item_ {
    construct new() {}
    call(key, value) {}
}
var store_item = Store_item_.new()
class Read_item_ {
    call(key) {}
var read_item = Read_item_.new()
store_item.call(1, 10)
read_item.call(1)
