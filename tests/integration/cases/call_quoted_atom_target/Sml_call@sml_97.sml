fun DoThing _ = ()
datatype val_t =
    SInt of LargeInt.int
  | SList of val_t list
val _ = DoThing(SInt 1)
val _ = DoThing(SInt 2)
