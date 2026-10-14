module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt (-2147483649);
    OInt (-2147483648);
    OInt 2147483647;
    OInt 2147483648
]

end
