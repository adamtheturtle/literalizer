module Check = struct

module Thing = struct
let first_value _ = ()
end
type val_t =
  | OInt of int
let _ = Thing.first_value(OInt 1)

end
