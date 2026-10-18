module Check = struct

type val_t =
  | OInt of int
  | OArray of val_t array
let my_data : val_t array = [|
    OInt 0;
    OInt 2147483648
|]

end
