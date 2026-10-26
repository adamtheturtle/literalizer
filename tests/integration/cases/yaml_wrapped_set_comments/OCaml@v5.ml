module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let my_data : val_t = OSet [
    OInt 10;  (* comment for ten *)
    OInt 2  (* comment for two *)
]

end
