structure thing = struct
fun first_value _ = ()
end
datatype val_t =
    SInt of LargeInt.int
val _ = thing.first_value(SInt 1)
