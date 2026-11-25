module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0o0;
    OInt 0o1;
    OInt (-0o1)
]

end
