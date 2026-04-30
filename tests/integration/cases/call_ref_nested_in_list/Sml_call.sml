datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun process _ = ()
val my_var : val_t = SInt 42
val my_other : val_t = SInt 7
val _ = process(SList [SMap [("ref", SStr "my_var")], SInt 42, SStr "static"])
val _ = process(SList [SMap [("ref", SStr "my_other")], SInt 7, SStr "label"])
