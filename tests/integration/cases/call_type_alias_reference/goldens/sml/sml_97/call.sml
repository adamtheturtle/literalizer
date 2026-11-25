datatype val_t =
    SInt of LargeInt.int
fun process _ = ()
val value : val_t = SInt 1
val _ = process(value)
