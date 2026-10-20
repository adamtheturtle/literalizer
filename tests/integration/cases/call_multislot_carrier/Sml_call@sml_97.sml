fun process _ = ()
datatype val_t =
    SNull
  | SBool of bool
  | SInt of LargeInt.int
  | SReal of real
  | SStr of string
  | SList of val_t list
val _ = process(SInt 1, SStr "hello")
val _ = process(SStr "two", SBool false)
val _ = process(SReal 3.5, SNull)
