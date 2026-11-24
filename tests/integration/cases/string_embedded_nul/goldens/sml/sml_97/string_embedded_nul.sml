datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("x", SStr "\000"),
    ("y", SStr "\0001")
]
val _ = my_data
