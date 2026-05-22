datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "café",
    SStr "中文"
]
val _ = my_data
