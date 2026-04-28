datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "100% done",
    SStr "%(name) is here"
]
val _ = my_data
