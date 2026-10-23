module Check = struct

type val_t =
  | ODate of (int * int * int)
  | OArray of val_t array
let my_data : val_t array = [|
    ODate (2024, 1, 15);
    ODate (2024, 2, 20)
|]

end
