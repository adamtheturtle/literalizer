datatype val_t =
    SNull
  | SList of val_t list
val value : val_t = SNull
val my_data : val_t = SList [
    value,
    value,
    SNull
]
val _ = my_data
