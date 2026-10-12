fun process _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = process(SInt 42)
