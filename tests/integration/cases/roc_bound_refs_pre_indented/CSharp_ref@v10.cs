using System;
using System.Collections.Generic;
            var Shared = (
                1,
                2
            );
            var Other = 3;
            var Payload = "\n    shared : Val\nshared = RInt 99";
            var my_data = new Dictionary<string, object> {
                ["a"] = Shared,
                ["b"] = Other,
                ["payload"] = Payload
            };
