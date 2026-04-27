structure Check = struct

datatype val_t =
    SInt of LargeInt.int
fun process _ = ()
val _ = process(1)

end
