module Check = struct

let my_data : Yojson.Safe.t = `List [
    `List [`List []; `List []];
    `List [`List [`Int 1]; `List [`Int 1]]
]

end
