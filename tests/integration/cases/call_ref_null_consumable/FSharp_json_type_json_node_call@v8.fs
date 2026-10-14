module Main

open System.Text.Json.Nodes
let consume (_value: obj) : obj = null
let my_null: JsonNode = null
let regular_null: JsonNode = null
consume(my_null) |> ignore
consume(regular_null) |> ignore
