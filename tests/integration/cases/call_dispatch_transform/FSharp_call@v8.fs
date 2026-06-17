module Main

type Val =
    | FInt of int64
    | FList of Val list
let record_value (_value: obj) : obj = null
let flush_buffer (_count: obj) : obj = null
let emit (__arg: obj) : obj = null
emit(record_value(42))
flush_buffer(3)
