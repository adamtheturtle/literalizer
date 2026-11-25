module Check = struct

type val_t =
  | ONull
  | OBool of bool
  | OInt of int
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OBool true;
    OStr "hi";
    OArray [|OInt 1; OInt 2|];
    ONull
|]

end
