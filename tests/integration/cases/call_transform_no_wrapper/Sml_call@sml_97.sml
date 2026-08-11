datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process(SStr "hello")
val _ = process(SInt 42)
val _ = process(SBool true)
