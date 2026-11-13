typedef enum int {_VVAL_BOOL, _VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
typedef struct {
    string k;
    _VVal v;
} _VKV;
module main;
initial begin
static _VKV my_data[] = '{
    _VKV'{k: "true_to_one", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "one_to_true", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_BOOL, i: 1, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "false_to_zero", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "zero_to_false", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_BOOL, i: 0, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "nested_boolean_to_float", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_REAL, i: 0, r: 1.0, s: \\\"\\\"}}\"}}}"}},
    _VKV'{k: "nested_float_to_boolean", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_BOOL, i: 0, r: 0.0, s: \\\"\\\"}}\"}}}"}},
    _VKV'{k: "nested_value_types_changed", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"nested\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{_VVal'{tag: _VVAL_BOOL, i: 1, r: 0.0, s: \\\\\\\"\\\\\\\"}, _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: \\\\\\\"\\\\\\\"}}\\\"}}}\"}}}"}},
    _VKV'{k: "nested_value_types_reversed", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"nested\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\\\\\"\\\\\\\"}, _VVal'{tag: _VVAL_BOOL, i: 0, r: 0.0, s: \\\\\\\"\\\\\\\"}}\\\"}}}\"}}}"}},
    _VKV'{k: "array_order_changed", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}}\"}}}"}},
    _VKV'{k: "array_length_changed", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \\\"\\\"}}\"}}}"}},
    _VKV'{k: "null_to_zero", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "string_to_boolean", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_BOOL, i: 1, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "object_key_changed", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"b\\\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}}}\"}}}"}}
};
end
endmodule
