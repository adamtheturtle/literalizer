module Main

type ThingType_() =
    member _.go() : obj = null
let thing = ThingType_()
type Val =
    | FList of Val list
thing.go()
