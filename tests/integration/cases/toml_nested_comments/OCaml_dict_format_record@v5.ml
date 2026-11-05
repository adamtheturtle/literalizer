module Check = struct

type val_t1 = { first : int; second : int }
type val_t2 = { name : string }
type val_t3 = { inner : int }
type val_t0 = { dotted : val_t1; plain : int; entries : val_t2 list; table : val_t3 }
let my_data = ({
    dotted = ({
        first = 1;
        second = 2
    } : val_t1);
    plain = 3;
    entries = [
        ({
            name = "one"
        } : val_t2);
        ({
            name = "two"
        } : val_t2)
    ];
    table = ({
        inner = 4
    } : val_t3)
} : val_t0)

end
