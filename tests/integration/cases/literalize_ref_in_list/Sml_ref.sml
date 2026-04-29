datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val val_x : val_t = SMap [
    ("_", SStr "_")
]
val val_y : val_t = SMap [
    ("_", SStr "_")
]
val my_data : val_t = SList [
    val_x,
    val_y
]
val _ = my_data
