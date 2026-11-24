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
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"input\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"name\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"alice\\\"}}, _VKV'{k: \\\"city\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"paris\\\"}}}\"}}, _VKV'{k: \"expected\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"count\\\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}}, _VKV'{k: \\\"total\\\", v: _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \\\"\\\"}}}\"}}}"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"input\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"name\\\", v: _VVal'{tag: _VVAL_INT, i: 10, r: 0.0, s: \\\"\\\"}}, _VKV'{k: \\\"city\\\", v: _VVal'{tag: _VVAL_INT, i: 20, r: 0.0, s: \\\"\\\"}}}\"}}, _VKV'{k: \"expected\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"count\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"done\\\"}}, _VKV'{k: \\\"total\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"pending\\\"}}}\"}}}"}
};
end
endmodule
