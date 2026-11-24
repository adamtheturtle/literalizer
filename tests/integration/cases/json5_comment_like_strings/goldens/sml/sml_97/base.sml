datatype val_t =
    SStr of string
  | SList of val_t list
val my_data : val_t = SList [
    SStr "// data",
    SStr "/* data */",
    SStr "escaped quote: \" // data",
    SStr "backslash: \\"
]
val _ = my_data
