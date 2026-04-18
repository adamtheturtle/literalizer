structure Check = struct

datatype val_t =
    SInt of int
val my_data : val_t = SInt 2147483648

end
