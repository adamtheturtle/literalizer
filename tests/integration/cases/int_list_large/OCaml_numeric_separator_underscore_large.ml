module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 1_000_000;
    OInt (-1_234);
    OInt 255;
    OInt (-10)
]

end
