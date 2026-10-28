module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt (-0o20000000000);
    OInt (-0o17777777777);
    OList [OInt 0o0]
]

end
