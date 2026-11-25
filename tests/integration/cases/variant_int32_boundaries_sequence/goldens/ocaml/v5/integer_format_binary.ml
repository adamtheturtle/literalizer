module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt (-0b10000000000000000000000000000000);
    OInt (-0b1111111111111111111111111111111);
    OList [OInt 0b0]
]

end
