datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process(42), 1)
