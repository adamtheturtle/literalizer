datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val shared_var : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = SList [
    shared_var,
    shared_var
]
val _ = my_data
