module Check = struct

type val_t =
  | OInt of int
let my_int : val_t = OInt 42
let my_data : val_t = my_int

end
