structure class = struct
fun member _ = ()
end
datatype val_t =
    SInt of LargeInt.int
val _ = class.member(SInt 42)
