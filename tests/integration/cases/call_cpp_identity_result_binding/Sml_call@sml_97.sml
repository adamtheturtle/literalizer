structure thing = struct
fun go _ = ()
end
datatype val_t =
    SList of val_t list
val my_data = thing.go(SList [])
val _ = my_data
