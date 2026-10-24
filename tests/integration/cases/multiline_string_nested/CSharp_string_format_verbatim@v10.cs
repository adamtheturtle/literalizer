using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object?> {
    [@"outer"] = ValueTuple.Create(ValueTuple.Create(@"nested first line
  indented

nested last line
"))
};
    _ = my_data;
