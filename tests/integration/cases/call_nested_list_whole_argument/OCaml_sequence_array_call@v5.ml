module Check = struct

let f _ = ()
type val_t =
  | OInt of int
  | OArray of val_t array
let _ = f([|OArray [|OInt 1; OInt 2|]; OArray [|OInt 3|]|])

end
