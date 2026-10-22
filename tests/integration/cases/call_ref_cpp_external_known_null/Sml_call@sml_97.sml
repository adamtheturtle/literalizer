datatype val_t =
    SNull
fun consume _ = ()
val item : val_t = SNull
val _ = consume(item)
