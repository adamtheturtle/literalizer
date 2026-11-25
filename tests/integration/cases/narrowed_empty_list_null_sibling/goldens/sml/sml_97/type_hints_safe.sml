datatype val_t =
    SNull
  | SList of val_t list
val my_data : val_t = SList [
    SList [SNull],
    SList []
]
val _ = my_data
