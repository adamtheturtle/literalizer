module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("v", `String "a﻿b")
]

end
