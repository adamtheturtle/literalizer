module Check = struct

type val_t =
  | OInt of int
  | OArray of val_t array
let array_value : val_t array = [|
    OInt 1;
    OInt 2
|]
let scalar_value : val_t = OInt 3
let my_data : val_t array = [|
    OArray array_value;
    scalar_value
|]

end
