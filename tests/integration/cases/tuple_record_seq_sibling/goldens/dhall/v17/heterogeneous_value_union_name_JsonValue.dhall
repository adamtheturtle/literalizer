let JsonValue = < Int : Integer | Str : Text > in
let my_data = {
  scores = [JsonValue.Int +10, JsonValue.Int +20, JsonValue.Int +30],
  args = [JsonValue.Int +1, JsonValue.Str "email", JsonValue.Str "a@gmail.com", JsonValue.Int +100],
} in my_data
