module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let my_data : val_t = OSet [
    OInt 0x1;
    OInt 0x2;
    OInt 0x3
]

end
