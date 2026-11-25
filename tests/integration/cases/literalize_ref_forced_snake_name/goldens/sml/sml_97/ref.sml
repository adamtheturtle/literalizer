datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val user_obj : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = user_obj
val _ = my_data
