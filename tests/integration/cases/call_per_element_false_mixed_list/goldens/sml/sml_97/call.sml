datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process(SList [SInt 1, SStr "x"])
