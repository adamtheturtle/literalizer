module Check = struct

type val_t =
  | OInt of int
let my_data : val_t = OInt 2_147_483_648

end
