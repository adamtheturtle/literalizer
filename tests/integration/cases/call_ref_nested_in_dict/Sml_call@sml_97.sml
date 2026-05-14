datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun process _ = ()
val my_var : val_t = SInt 42
val _ = process(SMap [("key", my_var), ("count", SInt 42)])
