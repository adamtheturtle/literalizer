datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [SList [SMap [("$ref", SStr "my_var")], SInt 42, SStr "static"]],
    SList [SList [SMap [("$ref", SStr "my_other")], SInt 7, SStr "label"]]
]
val _ = my_data
