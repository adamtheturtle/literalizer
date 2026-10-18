using System.Collections.Generic;
using System;
var my_data = (
    (
        new Dictionary<string, object?> {
            ["values"] = ValueTuple.Create(
                ValueTuple.Create()
            )
        },
        new Dictionary<string, object?> {}
    ),
    (
        new Dictionary<string, object?> {},
        new Dictionary<string, object?> {
            ["values"] = ValueTuple.Create(
                ValueTuple.Create()
            )
        }
    )
);
    _ = my_data;
