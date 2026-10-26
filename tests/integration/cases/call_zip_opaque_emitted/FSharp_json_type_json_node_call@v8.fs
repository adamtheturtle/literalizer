module Main

open System.Text.Json.Nodes
let ``process`` (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(``process``((JsonValue.Create(1L) :> JsonNode)), (JsonValue.Create("2024-01-15T12:00:00") :> JsonNode)) |> ignore
