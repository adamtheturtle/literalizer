datatype val_t =
    SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun process _ = ()
val big_list : val_t = SList [
    SStr "x"
]
val _ = process(SMap [("m", big_list)])
