module Main

type Val =
    | FNull
let consume (_value: obj) : obj = null
let value: Val = FNull
consume(value)
