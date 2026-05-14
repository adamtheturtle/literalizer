datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("times", SList ["09:30:00", "17:45:00", "23:59:59"])
]
val _ = my_data
