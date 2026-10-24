module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0x1;
    OStr "email";
    OStr "a@gmail.com";
    OInt 0x64
]

end
