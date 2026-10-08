datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val actual : val_t = SInt 42
val my_data : val_t = SList [
    SMap [("$ref", SInt 1)],
    SMap [("$ref", SNull)],
    actual
]
val _ = my_data
