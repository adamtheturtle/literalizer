module Main

type FoobarType_() =
    member _.bar(_x: obj) : obj = null
type Foo_BarType_() =
    member _.fooBar = FoobarType_()
type AType_() =
    member _.foo_bar = Foo_BarType_()
let a = AType_()
type Val =
    | FInt of int64
    | FList of Val list
a.foo_bar.fooBar.bar(FList [FInt 1L]) |> ignore
