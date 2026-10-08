module Main

type OuterType_() =
    member _.inner(_outer: obj, _n: obj) : obj = null
let outer = OuterType_()
type Val =
    | FInt of int64
    | FList of Val list
outer.inner(FInt 1L, FInt 2L)
