datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun process _ = ()
fun emit _ = ()
val _ = emit(process(SStr "hello"), SMap [("a", SInt 1), ("b", SInt 2)])
val _ = emit(process(SInt 42), SMap [("c", SInt 3), ("d", SInt 4)])
