module Check = struct

type val_t =
  | ONull
let item : val_t = ONull
let my_data : val_t = ONull
(void)my_data;
let my_data : val_t = item
(void)my_data;

end
