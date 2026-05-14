let Value = < Int : Integer | Str : Text > in
let my_data = {
  a = Value.Int +1,
  b = Value.Int +3000000000,
  c = Value.Str "x",
} in my_data
