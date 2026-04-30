datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SList [SMap [("key", SMap [("$ref", SStr "my_var")]), ("count", SInt 42)]]
]
val _ = my_data
