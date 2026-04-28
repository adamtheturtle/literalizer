datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "prefix ${HOME} suffix",
    SStr "${interpolated}"
]
val _ = my_data
