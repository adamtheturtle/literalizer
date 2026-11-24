module Check = struct

type val_t1 = { name : string; active : bool }
type val_t2 = { name : string; score : float }
type val_t0 = { owner : val_t1; members : val_t2 list }
let my_data = ({
    owner = ({
        name = "Ada";
        active = false
    } : val_t1);
    members = [
        ({
            name = "Ada";
            score = 1.5
        } : val_t2);
        ({
            name = "Bob";
            score = 2.5
        } : val_t2)
    ]
} : val_t0)

end
