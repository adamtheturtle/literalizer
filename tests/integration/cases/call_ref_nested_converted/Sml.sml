datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [SList [SMap [("$ref", SStr "myVar")], SInt 42, SStr "static"]]
]
val _ = my_data
