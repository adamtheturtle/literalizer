datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("nested", SMap [("times", SList [SStr "1900-01-01T00:00:00+00:00"])])],
    SMap []
]
val _ = my_data
