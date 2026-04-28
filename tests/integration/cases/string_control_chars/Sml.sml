datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "line1\r\nline2",
    SStr "line1\rline2",
    SStr "\001"
]
val _ = my_data
