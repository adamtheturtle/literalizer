let JsonValue = < Int : Integer | Str : Text > in
let my_data = {
  a = JsonValue.Int +1,
  b = JsonValue.Int +3000000000,
  c = JsonValue.Str "x",
} in my_data
