module Main

type FooType_2() =
    member _.bar(_x: obj) : obj = null
type FooType_1() =
    member _.Foo = FooType_2()
type AType_() =
    member _.foo = FooType_1()
let a = AType_()
type Val =
    | FInt of int64
    | FList of Val list
let my_data = a.foo.Foo.bar(FList [FInt 1L])
