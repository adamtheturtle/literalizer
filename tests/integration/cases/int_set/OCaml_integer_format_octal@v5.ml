module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let my_data : val_t = OSet [
    OInt 0o1;
    OInt 0o2;
    OInt 0o3
]

end
