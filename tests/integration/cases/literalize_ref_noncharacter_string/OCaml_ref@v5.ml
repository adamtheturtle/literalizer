module Check = struct

type val_t =
  | OStr of string
let source_value : val_t = OStr "￾￿"
let my_data : val_t = source_value

end
