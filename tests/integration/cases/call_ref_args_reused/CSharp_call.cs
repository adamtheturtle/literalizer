using System;
class Check {
static object process(object data = null, object count = null) => null;
    public static void Main() {
var shared = 1;
var other = 2;
process(shared, 1);
process(other, 0);
process(shared, 8);
    }
}
