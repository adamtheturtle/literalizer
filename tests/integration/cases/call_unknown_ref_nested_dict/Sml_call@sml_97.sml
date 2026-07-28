datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun process _ = ()
val my_list : val_t = SList []
val _ = process(SList [SList [SMap [("inner", my_list)]]])
