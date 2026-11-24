datatype val_t =
    SInt of LargeInt.int
fun consume _ = ()
val shared : val_t = SInt 42
val _ = consume(shared)
