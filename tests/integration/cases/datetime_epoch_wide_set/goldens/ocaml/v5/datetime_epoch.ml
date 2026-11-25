module Check = struct

type val_t =
  | OInt of int
  | OSet of val_t list
let my_data : val_t = OSet [
    OInt 4085195400
]

end
