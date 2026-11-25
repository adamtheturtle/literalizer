module Check = struct

type val_t =
  | OBool of bool
  | OInt of int
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OInt 1;
    OStr "hello";
    OBool true
|]

end
