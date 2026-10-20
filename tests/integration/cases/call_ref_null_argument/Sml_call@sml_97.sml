datatype val_t =
    SNull
fun consume _ = ()
val value : val_t = SNull
val _ = consume(value)
