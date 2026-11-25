datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("timestamp", SStr "2040-01-01T03:00:00+03:00")],
    SMap []
]
val _ = my_data
