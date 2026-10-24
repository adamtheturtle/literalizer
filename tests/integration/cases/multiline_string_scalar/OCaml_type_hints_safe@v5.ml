module Check = struct

type val_t =
  | OStr of string
let my_data : val_t = OStr "\nroot first line\n  indented\n\nroot last line\n"

end
