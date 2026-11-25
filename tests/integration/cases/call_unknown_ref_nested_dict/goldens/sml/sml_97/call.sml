datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun process _ = ()
val my_list : val_t = SMap [
    ("unused", SStr "value")
]
val _ = process(SList [SList [SMap [("inner", my_list)]]])
