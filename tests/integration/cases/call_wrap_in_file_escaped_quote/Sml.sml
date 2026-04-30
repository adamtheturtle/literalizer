datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [SStr "a\"b"]
]
val _ = my_data
