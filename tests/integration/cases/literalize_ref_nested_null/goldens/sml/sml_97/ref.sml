datatype val_t =
    SNull
  | SList of val_t list
val my_null : val_t = SNull
val my_data : val_t = SList [
    my_null,
    SNull
]
val _ = my_data
