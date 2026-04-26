module Check = struct

type val_t =
  | OInt of int
let my_data : val_t = OInt (try int_of_string "-9223372036854775809" with Failure _ -> 0)

end
