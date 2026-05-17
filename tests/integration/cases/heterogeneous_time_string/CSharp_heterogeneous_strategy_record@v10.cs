using System;
using System.Collections.Generic;
record Record0(object[] Vals);
class Check {
    public static void Main() {
var my_data = new Record0(
    new object[] {
        new TimeOnly(9, 30, 0),
        "hello"
    }
);
    }
}
