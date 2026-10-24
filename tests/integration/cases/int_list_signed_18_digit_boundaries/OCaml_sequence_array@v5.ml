module Check = struct

type val_t =
  | OInt of int
  | OArray of val_t array
let my_data : val_t array = [|
    OInt 999999999999999999;
    OInt (-999999999999999999)
|]

end
