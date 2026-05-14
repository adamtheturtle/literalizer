datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "2024-01-15",
    SStr "2024-02-20"
]
val _ = my_data
