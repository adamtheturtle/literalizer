module Main

open System.Text.Json.Nodes
let private _mainDeclaration () =
    let mutable my_data: JsonNode = JsonObject(dict [
        ("name", (JsonValue.Create("Alice") :> JsonNode));
        ("scores", (JsonArray([|(JsonValue.Create(10L) :> JsonNode); (JsonValue.Create(20L) :> JsonNode); (JsonValue.Create(30L) :> JsonNode)|]) :> JsonNode))
    ])
    ignore my_data

let private _mainAssignment () =
    let my_data: JsonNode = JsonObject(dict [
        ("name", (JsonValue.Create("Alice") :> JsonNode));
        ("scores", (JsonArray([|(JsonValue.Create(10L) :> JsonNode); (JsonValue.Create(20L) :> JsonNode); (JsonValue.Create(30L) :> JsonNode)|]) :> JsonNode))
    ])
    ignore my_data
