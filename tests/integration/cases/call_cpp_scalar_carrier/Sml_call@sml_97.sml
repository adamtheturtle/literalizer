fun process _ = ()
datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SStr of string
  | SList of val_t list
val _ = process(SStr "hello")
val _ = process(SInt 42)
val _ = process(SBool true)
val _ = process(SNull)
