datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "1960-01-01T00:00:00+00:00"
]
val _ = my_data
