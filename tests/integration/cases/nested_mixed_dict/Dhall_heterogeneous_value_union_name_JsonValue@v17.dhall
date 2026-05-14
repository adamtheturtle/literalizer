let JsonValue = < Int : Integer | Str : Text | Null > in
let my_data = {
  outer = {a = JsonValue.Int +1, b = JsonValue.Str "x", c = JsonValue.Null},
} in my_data
