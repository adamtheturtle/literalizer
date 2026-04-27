structure Check = struct

datatype val_t =
    SInt of LargeInt.int
val my_data : val_t = SInt 0x80000000

end
