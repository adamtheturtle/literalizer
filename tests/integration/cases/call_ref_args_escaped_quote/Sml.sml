datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [SMap [("$ref", SStr "my_str")]]
]
val _ = my_data
