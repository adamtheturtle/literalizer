module Main

type FooType_() =
    member _.bar(_x: obj) : obj = null
type FooType_() =
    member _.Foo = FooType_()
let foo = FooType_()
type Val =
    | FInt of int64
    | FList of Val list
foo.Foo.bar(FList [FInt 1L]) |> ignore
