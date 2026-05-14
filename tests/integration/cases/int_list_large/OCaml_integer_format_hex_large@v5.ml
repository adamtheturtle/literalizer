module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0xf4240;
    OInt (-0x4d2);
    OInt 0xff;
    OInt (-0xa)
]

end
