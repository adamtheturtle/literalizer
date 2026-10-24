module Check = struct

type val_t =
  | OInt of int
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OArray [|OInt 1; OStr "two"|];
    OArray [||]
|]

end
