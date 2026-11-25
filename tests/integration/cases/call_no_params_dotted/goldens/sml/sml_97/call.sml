datatype val_t =
    SList of val_t list
structure throttler = struct
fun check _ = ()
end
val _ = throttler.check()
val _ = throttler.check()
