module Main

let store_item (_key: obj, _value: obj) : obj = null
let read_item (_key: obj) : obj = null
type Val =
    | FInt of int64
    | FList of Val list
store_item(1, 10)
read_item(1)
