module Check = struct

type val_t =
  | OInt of int
let stamp : val_t = OInt 1
let result_data : val_t = stamp

end
