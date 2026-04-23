let Value = < Str : Text | Int : Integer | Bool : Bool > in
let my_data = {
  name = Value.Str "Alice",
  age = Value.Int +30,
  active = Value.Bool True,
} in my_data
