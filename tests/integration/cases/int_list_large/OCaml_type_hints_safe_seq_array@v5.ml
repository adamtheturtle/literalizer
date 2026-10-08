module Check = struct

type val_t =
  | OInt of int
  | OArray of val_t array
let my_data : val_t array = [|
    OInt 1000000;
    OInt (-1234);
    OInt 255;
    OInt (-10)
|]

end
