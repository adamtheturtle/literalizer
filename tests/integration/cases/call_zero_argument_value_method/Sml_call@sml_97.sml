structure thing = struct
fun go _ = ()
end
datatype val_t =
    SList of val_t list
val _ = thing.go()
