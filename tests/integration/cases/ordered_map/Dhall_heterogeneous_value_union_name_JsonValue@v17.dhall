let JsonValue = < Str : Text | Int : Integer | Bool : Bool > in
let my_data = {
  name = JsonValue.Str "Alice",
  age = JsonValue.Int +30,
  active = JsonValue.Bool True,
} in my_data
