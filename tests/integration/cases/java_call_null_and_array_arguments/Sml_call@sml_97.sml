datatype val_t =
    SNull
  | SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val _ = process(SNull)
val _ = process(SList [SInt 1, SInt 2])
