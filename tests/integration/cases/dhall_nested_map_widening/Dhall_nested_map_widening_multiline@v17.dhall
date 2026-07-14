let Value = < Str : Text | Int : Integer > in
let my_data = [
  {
    input = {
      name = Value.Str "alice",
      city = Value.Str "paris",
    },
    expected = {
      count = Value.Int +1,
      total = Value.Int +2,
    },
  },
  {
    input = {
      name = Value.Int +10,
      city = Value.Int +20,
    },
    expected = {
      count = Value.Str "done",
      total = Value.Str "pending",
    },
  },
] in my_data
