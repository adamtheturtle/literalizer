let JsonValue = < Str : Text | Int : Integer | Bool : Bool | Double : Double > in
let my_data = {
  name = JsonValue.Str "Alice",
  age = JsonValue.Int +30,
  active = JsonValue.Bool True,
  score = JsonValue.Double 4.5,
} in my_data
