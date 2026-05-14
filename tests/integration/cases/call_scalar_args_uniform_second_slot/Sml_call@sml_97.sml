datatype val_t =
    SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
fun process _ = ()
val _ = process("hello", "a")
val _ = process(42, "b")
val _ = process(SBool true, "c")
