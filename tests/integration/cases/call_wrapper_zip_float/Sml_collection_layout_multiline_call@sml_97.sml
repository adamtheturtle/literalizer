datatype val_t =
    SInt of LargeInt.int
  | SReal of real
  | SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process(SInt 1), SReal 1.5)
