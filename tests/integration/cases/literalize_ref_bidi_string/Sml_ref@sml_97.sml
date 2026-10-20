datatype val_t =
    SStr of string
  | SMap of (string * val_t) list
val text : val_t = SStr "a\226\128\170b"
val my_data : val_t = SMap [
    ("value", text)
]
val _ = my_data
