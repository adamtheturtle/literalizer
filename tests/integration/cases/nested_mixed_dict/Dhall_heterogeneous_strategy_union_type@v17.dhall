let Value = < Int : Integer | Str : Text | Null > in
let my_data = {
  outer = {a = Value.Int +1, b = Value.Str "x", c = Value.Null},
} in my_data
