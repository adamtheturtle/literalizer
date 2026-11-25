datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process(SInt 1), SInt 42)
