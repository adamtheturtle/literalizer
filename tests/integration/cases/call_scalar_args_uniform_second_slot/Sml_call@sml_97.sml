datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process(SStr "hello", SStr "a")
val _ = process(SInt 42, SStr "b")
val _ = process(SBool true, SStr "c")
