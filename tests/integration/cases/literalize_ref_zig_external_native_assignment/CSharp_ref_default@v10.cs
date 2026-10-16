using System;
var shared = (
    1,
    2
);
var my_data = ValueTuple.Create(
    0
);
_ = &my_data;
my_data = shared;
_ = &my_data;
