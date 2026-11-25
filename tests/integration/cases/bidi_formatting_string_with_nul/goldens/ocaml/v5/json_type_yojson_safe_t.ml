module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("v", `String "a‪\000é😀b")
]

end
