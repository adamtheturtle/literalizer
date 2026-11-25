datatype val_t =
    SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
  | SMap of (string * val_t) list
fun consume _ = ()
val item : val_t = SInt 42
val _ = consume(SMap [("field", item)])
