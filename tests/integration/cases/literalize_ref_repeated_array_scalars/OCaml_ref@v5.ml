module Check = struct

type val_t =
  | OInt of int
  | OArray of val_t array
let shared : val_t array = [|
    OInt 1;
    OInt 2
|]
let my_data : val_t array = [|
    OArray shared;
    OArray shared
|]

end
