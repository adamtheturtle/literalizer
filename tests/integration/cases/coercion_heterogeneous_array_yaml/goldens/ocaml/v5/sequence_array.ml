module Check = struct

type val_t =
  | OInt of int
  | OFloat of float
  | OArray of val_t array
let my_data : val_t array = [|
    OInt 1;
    OFloat 2.5;
    OInt 3
|]

end
