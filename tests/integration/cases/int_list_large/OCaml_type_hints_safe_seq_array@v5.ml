module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t array = [|
    OInt 1000000;
    OInt (-1234);
    OInt 255;
    OInt (-10)
|]

end
