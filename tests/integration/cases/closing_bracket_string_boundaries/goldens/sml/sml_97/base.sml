datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "]",
    SStr "a]",
    SStr "a]=",
    SStr "a]b"
]
val _ = my_data
