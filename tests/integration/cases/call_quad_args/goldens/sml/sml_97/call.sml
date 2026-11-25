datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val _ = process(SInt 1, SInt 2, SInt 3, SInt 4)
val _ = process(SInt 5, SInt 6, SInt 7, SInt 8)
