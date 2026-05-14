module Main

type Val =
    | FList of Val list
let process () : obj = null
let emit (__arg: obj) : obj = null
emit(process())
emit(process())
