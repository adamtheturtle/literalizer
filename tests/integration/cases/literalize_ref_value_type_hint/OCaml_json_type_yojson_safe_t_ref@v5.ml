module Check = struct

let ref_data : Yojson.Safe.t = `List [
    `Int 1;
    `Int 2
]
let my_data : Yojson.Safe.t = ref_data

end
