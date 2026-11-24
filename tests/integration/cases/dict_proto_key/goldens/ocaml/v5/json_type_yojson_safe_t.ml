module Check = struct

let my_data : Yojson.Safe.t = `Assoc [
    ("__proto__", `Assoc [("x", `Int 1)]);
    ("n", `Assoc [("__proto__", `Int 3)]);
    ("y", `Int 2)
]

end
