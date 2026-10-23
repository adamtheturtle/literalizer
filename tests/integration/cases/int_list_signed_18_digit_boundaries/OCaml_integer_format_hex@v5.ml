module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0xde0b6b3a763ffff;
    OInt (-0xde0b6b3a763ffff)
]

end
