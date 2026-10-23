module Check = struct

type val_t =
  | OFloat of float
  | OArray of val_t array
let my_data : val_t array = [|
    OArray [|OFloat 1.5; OFloat 2.5|];
    OArray [|OFloat 3.5; OFloat 4.5|]
|]

end
