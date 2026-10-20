let JsonValue = < Int : Integer | Str : Text > in
let my_data = [
  [JsonValue.Int +1, JsonValue.Str "value"],
  [] : List JsonValue,
] in my_data
