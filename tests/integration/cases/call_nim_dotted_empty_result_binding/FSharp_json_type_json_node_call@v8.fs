module Main

type ThingType_() =
    member _.go(_value: obj) : obj = null
let thing = ThingType_()
open System.Text.Json.Nodes
let my_data = thing.go((JsonArray() :> JsonNode))
