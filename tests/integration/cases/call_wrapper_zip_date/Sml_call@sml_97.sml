datatype val_t =
    SInt of LargeInt.int
  | SDate of (int * int * int)
  | SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process(SInt 1), SDate (2024, 1, 15))
