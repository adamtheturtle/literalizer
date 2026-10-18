module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let my_data : val_t = OSet [
    OInt (-2147483649);
    OInt (-2147483648);
    OInt 2147483647;
    OInt 2147483648
]

end
