let JsonValue = < Int : Integer | Str : Text > in
let my_data = [
  {id = JsonValue.Int +1, label = JsonValue.Str "first"},
  {id = JsonValue.Int +2, label = JsonValue.Str "second"},
  {id = JsonValue.Int +3, label = JsonValue.Str "third"},
] in my_data
