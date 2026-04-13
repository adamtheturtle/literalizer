using System;
dynamic throttler = new System.Dynamic.ExpandoObject();
dynamic print(dynamic a) => null;
print(throttler.check("user_1", 1000.0));
print(throttler.check("user_2", 2000.5));
