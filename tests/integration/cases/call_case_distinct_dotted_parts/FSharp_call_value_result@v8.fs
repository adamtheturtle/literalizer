module Main

type FooType_() =
    member _.bar(_x: obj) : obj = null
type FooType_() =
    member _.Foo = FooType_()
type AType_() =
    member _.foo = FooType_()
let a = AType_()
type Val =
    | FInt of int64
    | FList of Val list
let my_data = a.foo.Foo.bar(FList [FInt 1L])
