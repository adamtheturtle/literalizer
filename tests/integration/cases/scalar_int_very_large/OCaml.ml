module Check = struct

type val_t =
  | OInt of int
let my_data : val_t = OInt (int_of_string "9223372036854775808")

end
