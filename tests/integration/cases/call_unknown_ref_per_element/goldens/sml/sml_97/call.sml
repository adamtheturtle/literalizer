datatype val_t =
    SList of val_t list
fun process _ = ()
val unknown_value : val_t = SList []
val _ = process(unknown_value)
