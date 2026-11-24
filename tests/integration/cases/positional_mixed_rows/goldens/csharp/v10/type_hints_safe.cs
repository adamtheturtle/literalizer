using System;
var my_data = (
    ((1, "value"), (1, 2), ValueTuple.Create()),
    (ValueTuple.Create(), ValueTuple.Create(), (3, 4))
);
    _ = my_data;
