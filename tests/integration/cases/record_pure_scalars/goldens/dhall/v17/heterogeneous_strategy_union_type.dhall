let Value = < Str : Text | Int : Integer | Bool : Bool | Double : Double > in
let my_data = {
  name = Value.Str "Alice",
  age = Value.Int +30,
  active = Value.Bool True,
  score = Value.Double 4.5,
} in my_data
