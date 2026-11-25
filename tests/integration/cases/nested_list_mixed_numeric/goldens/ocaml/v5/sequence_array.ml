module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OArray of val_t array
let my_data : val_t array = [|
    OArray [|OInt 1|];
    OArray [|OFloat 2.5|]
|]

end
