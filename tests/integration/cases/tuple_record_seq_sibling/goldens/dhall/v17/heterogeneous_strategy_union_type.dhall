let Value = < Int : Integer | Str : Text > in
let my_data = {
  scores = [Value.Int +10, Value.Int +20, Value.Int +30],
  args = [Value.Int +1, Value.Str "email", Value.Str "a@gmail.com", Value.Int +100],
} in my_data
