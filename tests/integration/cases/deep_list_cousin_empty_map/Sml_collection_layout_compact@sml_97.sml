datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
val my_data : val_t = SList [
    SMap [("items", SList [SMap [("inner", SMap [("x", SInt 1)])], SMap [("inner", SMap [])]])],
    SMap [("items", SList [SMap [("inner", SMap [("x", SInt 2)])], SMap [("inner", SMap [])]])]
]
val _ = my_data
