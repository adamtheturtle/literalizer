using System.Collections.Generic;
var my_data = new Dictionary<string, int> {
    ["user_name"] = 1,
    ["user.name"] = 2,
    ["user-name"] = 3,
    ["field_name_that_is_really_quite_long_one"] = 4,
    ["field_name_that_is_really_quite_long_two"] = 5
};
