module Main

open System.Text.Json.Nodes
let ``process`` (_value: obj) : obj = null
``process``((JsonValue.Create("hello") :> JsonNode)) |> ignore
``process``((JsonValue.Create(42L) :> JsonNode)) |> ignore
``process``((JsonValue.Create(true) :> JsonNode)) |> ignore
