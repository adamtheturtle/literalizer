datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SMap of (string * val_t) list
fun send _ = ()
val _ = send(SMap [("a", SInt 1), ("b", SStr "x")])
