datatype val_t =
    SInt of LargeInt.int
fun process _ = ()
fun emit _ = ()
val _ = emit(process(SInt 42))
