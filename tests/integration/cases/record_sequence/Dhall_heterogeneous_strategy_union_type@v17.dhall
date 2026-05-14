let Value = < Int : Integer | Str : Text > in
let my_data = [
  {id = Value.Int +1, label = Value.Str "first"},
  {id = Value.Int +2, label = Value.Str "second"},
  {id = Value.Int +3, label = Value.Str "third"},
] in my_data
