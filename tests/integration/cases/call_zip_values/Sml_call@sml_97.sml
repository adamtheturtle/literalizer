datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process("hello"), "one")
val _ = emit(process(42), "zero")
