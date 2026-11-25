using System;
var my_data = ValueTuple.Create(
    ValueTuple.Create(@"
first line
  indented

last line
")
);
    _ = my_data;
