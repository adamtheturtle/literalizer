module Check = struct

type val_t =
  | OFloat of float
  | OArray of val_t array
let my_data : val_t array = [|
    OFloat 1.1;
    OFloat (-2.2);
    OFloat 3.3
|]

end
