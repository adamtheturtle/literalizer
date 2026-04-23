using System;
dynamic throttler = new System.Dynamic.ExpandoObject();
dynamic emit(dynamic _a0) => null;
emit(throttler.check("user_1", 1000.0));
emit(throttler.check("user_2", 2000.5));
