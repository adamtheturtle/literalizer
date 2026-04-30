datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [SMap [("$ref", SStr "repeated_var")], SInt 1],
    SList [SMap [("$ref", SStr "single_var")], SInt 0],
    SList [SMap [("$ref", SStr "repeated_var")], SInt 8]
]
val _ = my_data
