structure outer = struct
structure thing = struct
fun go _ = ()
end
end
datatype val_t =
    SList of val_t list
val _ = outer.thing.go()
