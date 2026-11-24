module Check = struct

type val_t =
  | OStr of string
  | OArray of val_t array
let my_data : val_t array = [|
    OStr "100% done";
    OStr "%(name) is here"
|]

end
