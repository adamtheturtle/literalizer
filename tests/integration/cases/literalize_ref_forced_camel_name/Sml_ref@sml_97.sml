datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val userObj : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = userObj
val _ = my_data
