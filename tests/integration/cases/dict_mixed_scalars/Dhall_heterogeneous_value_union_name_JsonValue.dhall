let JsonValue = < Int : Integer | Str : Text > in
let my_data = {
  a = JsonValue.Int +1,
  b = JsonValue.Str "x",
} in my_data
