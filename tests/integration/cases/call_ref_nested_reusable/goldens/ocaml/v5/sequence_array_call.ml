module Check = struct

type val_t =
  | OInt of int
  | OArray of val_t array
let process _ = ()
let item : val_t array = [|
    OInt 1;
    OInt 2
|]
let _ = process([|OArray item; OArray item|])

end
