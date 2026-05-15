let Value = < Str : Text | Int : Integer | Double : Double | Bool : Bool | Null | Date : Text | DateTime : Text | Bytes : Text > in
let my_data = {
  s = Value.Str "string",
  i = Value.Int +1,
  f = Value.Double 1.5,
  b = Value.Bool True,
  n = Value.Null,
  d = Value.Date "2024-01-15",
  dt = Value.DateTime 1705320000,
  by = Value.Bytes "48656c6c6f",
} in my_data
