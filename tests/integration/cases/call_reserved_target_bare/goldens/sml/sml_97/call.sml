fun class _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = class(SInt 42)
