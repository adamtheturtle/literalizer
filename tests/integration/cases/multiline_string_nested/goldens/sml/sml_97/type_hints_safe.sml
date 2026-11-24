datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SMap [
    ("outer", SList [SList [SStr "nested first line\n  indented\n\nnested last line\n"]])
]
val _ = my_data
