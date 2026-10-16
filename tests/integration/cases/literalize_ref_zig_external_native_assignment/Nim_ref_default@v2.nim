var shared = @[
    1,
    2
]
var my_data = @[
    0
]
_ = &my_data;
my_data = shared
_ = &my_data;
