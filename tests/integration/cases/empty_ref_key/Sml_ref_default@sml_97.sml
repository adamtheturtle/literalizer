datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val external_value : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = SList [
    external_value
]
val _ = my_data
