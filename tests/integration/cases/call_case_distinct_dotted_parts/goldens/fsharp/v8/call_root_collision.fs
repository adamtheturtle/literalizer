module Main

type FooType_1() =
    member _.bar(_x: obj) : obj = null
type FooType_0() =
    member _.Foo = FooType_1()
let foo = FooType_0()
type Val =
    | FInt of int64
    | FList of Val list
foo.Foo.bar(FList [FInt 1L]) |> ignore
