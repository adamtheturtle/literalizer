datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
fun process _ = ()
val _ = process(SMap [("a", SInt 1), ("b", SInt 2)])
