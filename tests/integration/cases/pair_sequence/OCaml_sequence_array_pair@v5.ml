module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OInt 1;
    OStr "hello"
|]

end
