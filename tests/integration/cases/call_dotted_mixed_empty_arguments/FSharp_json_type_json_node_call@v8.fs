module Main

type ThingType_() =
    member _.go(_before: obj, _populated: obj, _after: obj) : obj = null
let thing = ThingType_()
open System.Text.Json.Nodes
thing.go((JsonArray() :> JsonNode), (JsonArray([|(JsonValue.Create(1L) :> JsonNode)|]) :> JsonNode), (JsonArray() :> JsonNode)) |> ignore
thing.go((JsonArray([|(JsonValue.Create("text") :> JsonNode)|]) :> JsonNode), (JsonArray([|(JsonValue.Create(2L) :> JsonNode)|]) :> JsonNode), (JsonArray() :> JsonNode)) |> ignore
thing.go((JsonArray() :> JsonNode), (JsonArray([|(JsonValue.Create("text") :> JsonNode)|]) :> JsonNode), (JsonArray() :> JsonNode)) |> ignore
thing.go((JsonArray([|(JsonValue.Create("text") :> JsonNode)|]) :> JsonNode), (JsonArray([|(JsonValue.Create(2L) :> JsonNode)|]) :> JsonNode), (JsonArray([|(JsonValue.Create(3L) :> JsonNode)|]) :> JsonNode)) |> ignore
