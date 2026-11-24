fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = process(SList [
    SInt 1,
    SInt 2
])
val _ = process(SList [
    SInt 3
])
