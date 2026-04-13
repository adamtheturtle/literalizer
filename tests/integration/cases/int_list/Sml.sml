structure Check = struct

datatype val_t =
    SInt of int
  | SList of val_t list
val my_data : val_t = SList [
    SInt 1,
    SInt 2,
    SInt 3
]

end
