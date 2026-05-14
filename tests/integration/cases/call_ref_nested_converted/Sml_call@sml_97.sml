datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
val my_var : val_t = SInt 42
val _ = process(SList [my_var, SInt 42, SStr "static"])
