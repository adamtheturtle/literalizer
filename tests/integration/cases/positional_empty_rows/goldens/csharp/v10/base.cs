using System;
var my_data = (
    ((1, "value"), ValueTuple.Create()),
    (ValueTuple.Create(), (2, "other"))
);
    _ = my_data;
