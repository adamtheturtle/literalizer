module Main

open System.Text.Json.Nodes
let mutable shared: JsonNode = null
let mutable my_data: JsonNode = shared
