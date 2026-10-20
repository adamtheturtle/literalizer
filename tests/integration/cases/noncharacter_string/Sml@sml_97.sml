datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("fffe", SStr "\239\191\190"),
    ("ffff", SStr "\239\191\191")
]
val _ = my_data
