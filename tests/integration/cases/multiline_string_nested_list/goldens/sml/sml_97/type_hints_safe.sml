datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SList [SStr "\nfirst line\n  indented\n\nlast line\n"]
]
val _ = my_data
