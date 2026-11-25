module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("a", `List [`Assoc [("item", `List [`Int 1])]]);
    ("b", `List [`Assoc [("item", `List [`Int 2; `Int 3])]])
]

end
