module Check = struct

type val_t =
  | OInt of int
  | OList of val_t list
let my_data : val_t = OList [
    OInt 0b11110100001001000000;
    OInt (-0b10011010010);
    OInt 0b11111111;
    OInt (-0b1010)
]

end
