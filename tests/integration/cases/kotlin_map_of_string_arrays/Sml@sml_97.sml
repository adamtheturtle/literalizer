datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("a", SList [SStr "x"]),
    ("b", SList [SStr "y"])
]
val _ = my_data
