fun BEGIN _ = ()
datatype val_t =
    SInt of LargeInt.int
val _ = BEGIN(SInt 42)
