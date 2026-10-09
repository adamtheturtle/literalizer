module Main

type ThingType_() =
    member _.go() : obj = null
type OuterType_() =
    member _.thing = ThingType_()
let outer = OuterType_()
type Val =
    | FList of Val list
outer.thing.go()
