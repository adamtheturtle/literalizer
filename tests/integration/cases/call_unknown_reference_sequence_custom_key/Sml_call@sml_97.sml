datatype val_t =
    SList of val_t list
fun process _ = ()
val untyped_value : val_t = SList []
val _ = process(SList [untyped_value, untyped_value])
