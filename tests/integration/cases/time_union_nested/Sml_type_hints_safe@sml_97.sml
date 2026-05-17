datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("mixed", SList [SList [SStr "09:30:00"], SList []])
]
val _ = my_data
