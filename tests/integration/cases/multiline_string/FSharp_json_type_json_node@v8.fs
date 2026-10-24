module Main

open System.Text.Json.Nodes
let my_data: JsonNode = JsonArray([|
    (JsonValue.Create("first line\n  indented\n\nlast line") :> JsonNode);
    (JsonValue.Create("\nleading newline") :> JsonNode);
    (JsonValue.Create(" \t\nleading whitespace") :> JsonNode);
    (JsonValue.Create("trailing newline\n") :> JsonNode);
    (JsonValue.Create("\nleading and trailing\n") :> JsonNode);
    (JsonValue.Create("quotes: \"\"\" ''' ` and backslash: \\") :> JsonNode);
    (JsonValue.Create("interpolation: ${value} #{value} #@value #$value $value") :> JsonNode);
    (JsonValue.Create("backslash before newline: \\\nnext line") :> JsonNode);
    (JsonValue.Create("trailing spaces  \nnext") :> JsonNode);
    (JsonValue.Create("C++ empty delimiter collision: )\"\nvalue") :> JsonNode);
    (JsonValue.Create("C++ first fallback collision: )\" and )x\"\nvalue") :> JsonNode);
    (JsonValue.Create("C++ second fallback collision: )\" and )x\" and )x0\"\nvalue") :> JsonNode);
    (JsonValue.Create("Rust delimiter collision: \"#\nvalue") :> JsonNode);
    (JsonValue.Create("Lua delimiter collision: ]]\nvalue") :> JsonNode);
    (JsonValue.Create("Swift delimiter collision: \"\"\"#\nvalue") :> JsonNode);
    (JsonValue.Create("Swift interpolation collision: \\#(value)\nvalue") :> JsonNode);
    (JsonValue.Create("Ruby fallback interpolation  \n#{expression} #@instance #$global") :> JsonNode);
    (JsonValue.Create("NUL followed by a digit: \0007") :> JsonNode);
    (JsonValue.Create("carriage\rreturn") :> JsonNode)
|])
