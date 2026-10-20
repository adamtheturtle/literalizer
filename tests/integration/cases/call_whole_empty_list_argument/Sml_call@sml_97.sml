fun f _ = ()
datatype val_t =
    SList of val_t list
val _ = f(SList [])
