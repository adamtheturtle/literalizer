module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt (-0x80000000);
    OInt (-0x7fffffff);
    OList [OInt 0x0]
]

end
