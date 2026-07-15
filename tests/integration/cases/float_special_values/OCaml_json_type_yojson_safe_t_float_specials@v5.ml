module Check = struct

let my_data : Yojson.Safe.t = `List [
    `Float infinity;
    `Float neg_infinity;
    `Float nan
]

end
