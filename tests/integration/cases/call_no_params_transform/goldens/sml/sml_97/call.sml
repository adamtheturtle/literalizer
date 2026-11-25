datatype val_t =
    SList of val_t list
fun process _ = ()
fun emit _ = ()
val _ = emit(process())
val _ = emit(process())
