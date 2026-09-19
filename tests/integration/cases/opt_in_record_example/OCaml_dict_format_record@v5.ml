module Check = struct

type val_t0 = { name : string; active : bool; scores : int list }
let my_data = ({
    name = "Ada";
    active = true;
    scores = [
        1;
        2;
        3
    ]
} : val_t0)

end
