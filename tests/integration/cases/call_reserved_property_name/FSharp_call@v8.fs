module Main

type Val =
    | FInt of int64
    | FList of Val list
type FooType_() =
    member _.class(_value: obj) : obj = null
let foo = FooType_()
foo.class(FInt 1L)
