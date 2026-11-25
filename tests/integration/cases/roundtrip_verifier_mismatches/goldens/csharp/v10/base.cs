using System.Collections.Generic;
using System;
var my_data = new Dictionary<string, object> {
    ["true_to_one"] = new Dictionary<string, object> {["value"] = 1},
    ["one_to_true"] = new Dictionary<string, object> {["value"] = true},
    ["false_to_zero"] = new Dictionary<string, object> {["value"] = 0},
    ["zero_to_false"] = new Dictionary<string, object> {["value"] = false},
    ["nested_boolean_to_float"] = new Dictionary<string, object> {["value"] = ValueTuple.Create(1.0)},
    ["nested_float_to_boolean"] = new Dictionary<string, object> {["value"] = ValueTuple.Create(false)},
    ["nested_value_types_changed"] = new Dictionary<string, object> {["value"] = new Dictionary<string, object> {["nested"] = (true, 0)}},
    ["nested_value_types_reversed"] = new Dictionary<string, object> {["value"] = new Dictionary<string, object> {["nested"] = (1, false)}},
    ["array_order_changed"] = new Dictionary<string, object> {["value"] = (2, 1)},
    ["array_length_changed"] = new Dictionary<string, object> {["value"] = (1, 2)},
    ["null_to_zero"] = new Dictionary<string, object> {["value"] = 0},
    ["string_to_boolean"] = new Dictionary<string, object> {["value"] = true},
    ["object_key_changed"] = new Dictionary<string, object> {["value"] = new Dictionary<string, object> {["b"] = 1}}
};
    _ = my_data;
