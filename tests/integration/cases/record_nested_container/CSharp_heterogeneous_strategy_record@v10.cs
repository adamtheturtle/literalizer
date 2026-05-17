using System.Collections.Generic;
using System;
record Record0(string Title, string[] Tags, int Priority);
class Check {
    public static void Main() {
var my_data = new Record0(
    "report",
    new string[] {
        "draft",
        "urgent",
        "review"
    },
    2
);
    }
}
