structure Check = struct

datatype val_t =
    SInt of int
  | SList of val_t list
val my_data : val_t = SList [
    SList [SList [SInt 1, SInt 2], SList [SInt 3, SInt 4]],
    SList [SList [SInt 5]]
]

end
