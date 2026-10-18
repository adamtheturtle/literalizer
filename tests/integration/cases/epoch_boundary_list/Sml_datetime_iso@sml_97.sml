datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "1901-12-13T20:45:51",
    SStr "1901-12-13T20:45:52",
    SStr "2038-01-19T03:14:07",
    SStr "2038-01-19T03:14:08"
]
val _ = my_data
