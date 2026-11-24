let JsonValue = < Str : Text | Int : Integer | Double : Double | Bool : Bool | Null | Date : Text | DateTime : Text | Bytes : Text > in
let my_data = {
  s = JsonValue.Str "string",
  i = JsonValue.Int +1,
  f = JsonValue.Double 1.5,
  b = JsonValue.Bool True,
  n = JsonValue.Null,
  d = JsonValue.Date "2024-01-15",
  dt = JsonValue.DateTime "2024-01-15T12:00:00",
  by = JsonValue.Bytes "48656c6c6f",
} in my_data
