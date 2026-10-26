datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "48656c6c6f",
    SList []
]
val _ = my_data
