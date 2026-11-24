module Check = struct

type val_t =
  | OBool of bool
let ref_flag : val_t = OBool true
let my_data : val_t = ref_flag

end
