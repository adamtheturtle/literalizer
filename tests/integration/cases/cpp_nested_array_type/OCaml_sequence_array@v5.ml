module Check = struct

type val_t =
  | OInt of int
  | OArray of val_t array
let my_data : val_t array = [|
    OArray [|OArray [|OInt 1|]|]
|]

end
