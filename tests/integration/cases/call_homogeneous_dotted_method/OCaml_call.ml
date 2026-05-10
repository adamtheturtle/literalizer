module Check = struct

type val_t =
  | OStr of string
  | OList of val_t list
module App = struct
module Client = struct
let fetch _ = ()
end
end
let _ = App.Client.fetch("hello")
let _ = App.Client.fetch("world")

end
