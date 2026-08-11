using System.Collections.Generic;
using System;
class Check {
static object consume(object items = null, object mapping = null) => null;
    public static void Main() {
var foo = 42;
consume((
    new Dictionary<string, object> {
        ["other"] = 1
    },
    foo
), new Dictionary<string, int> {
    ["left"] = foo,
    ["other"] = 1
});
    }
}
