datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process(SInt 1), SStr "2024-01-15T12:00:00")
