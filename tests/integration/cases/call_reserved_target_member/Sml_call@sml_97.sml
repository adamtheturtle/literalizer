structure obj = struct
fun class _ = ()
end
datatype val_t =
    SInt of LargeInt.int
val _ = obj.class(SInt 42)
