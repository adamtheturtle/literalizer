datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_var : val_t = SMap [
    ("_", SStr "_")
]
val item_var : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = SMap [
    ("key", my_var),
    ("items", SList [item_var, SMap [("fallback", SStr "value")]])
]
val _ = my_data
