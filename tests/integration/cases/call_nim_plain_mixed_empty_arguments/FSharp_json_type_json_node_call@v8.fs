module Main

let make_widget (_before: obj, _populated: obj, _after: obj) : obj = null
open System.Text.Json.Nodes
make_widget((JsonArray() :> JsonNode), (JsonArray([|(JsonValue.Create(1L) :> JsonNode)|]) :> JsonNode), (JsonArray() :> JsonNode)) |> ignore
make_widget((JsonArray([|(JsonValue.Create("text") :> JsonNode)|]) :> JsonNode), (JsonArray([|(JsonValue.Create(2L) :> JsonNode)|]) :> JsonNode), (JsonArray() :> JsonNode)) |> ignore
make_widget((JsonArray() :> JsonNode), (JsonArray([|(JsonValue.Create("text") :> JsonNode)|]) :> JsonNode), (JsonArray() :> JsonNode)) |> ignore
make_widget((JsonArray([|(JsonValue.Create("text") :> JsonNode)|]) :> JsonNode), (JsonArray([|(JsonValue.Create(2L) :> JsonNode)|]) :> JsonNode), (JsonArray([|(JsonValue.Create(3L) :> JsonNode)|]) :> JsonNode)) |> ignore
