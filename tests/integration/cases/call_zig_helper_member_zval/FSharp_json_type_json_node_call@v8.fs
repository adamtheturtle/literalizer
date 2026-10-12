module Main

open System.Text.Json.Nodes
type ObjType_() =
    member _.ZVal(_value: obj) : obj = null
let obj = ObjType_()
obj.ZVal((JsonValue.Create(1L) :> JsonNode))
