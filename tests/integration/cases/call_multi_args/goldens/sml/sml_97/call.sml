datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
val _ = process(SInt 1, SInt 42)
val _ = process(SInt 2, SInt 100)
