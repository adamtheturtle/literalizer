module Main

type ThingType_() =
    member _.go(_value: obj) : obj = null
let thing = ThingType_()
type Val =
    | FList of Val list
let my_data = thing.go(FList [])
