typedef enum int {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
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
    _VKV'{k: "level1", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"level2\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"level3\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{_VKV'{k: \\\\\\\"level4\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"'{_VKV'{k: \\\\\\\\\\\\\\\"value\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\"deep\\\\\\\\\\\\\\\"}}, _VKV'{k: \\\\\\\\\\\\\\\"items\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"a\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"b\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}}\\\\\\\\\\\\\\\"}}}\\\\\\\"}}}\\\"}}, _VKV'{k: \\\"sibling\\\", v: _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: \\\"\\\"}}}\"}}, _VKV'{k: \"tags\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{_VKV'{k: \\\\\\\"name\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"tag1\\\\\\\"}}, _VKV'{k: \\\\\\\"meta\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"'{_VKV'{k: \\\\\\\\\\\\\\\"priority\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\"}}, _VKV'{k: \\\\\\\\\\\\\\\"labels\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"x\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"y\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}}\\\\\\\\\\\\\\\"}}}\\\\\\\"}}}\\\"}}\"}}}"}}
};
my_data = '{
    _VKV'{k: "level1", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"level2\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"level3\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{_VKV'{k: \\\\\\\"level4\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"'{_VKV'{k: \\\\\\\\\\\\\\\"value\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\"deep\\\\\\\\\\\\\\\"}}, _VKV'{k: \\\\\\\\\\\\\\\"items\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"a\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"b\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}}\\\\\\\\\\\\\\\"}}}\\\\\\\"}}}\\\"}}, _VKV'{k: \\\"sibling\\\", v: _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: \\\"\\\"}}}\"}}, _VKV'{k: \"tags\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{_VKV'{k: \\\\\\\"name\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"tag1\\\\\\\"}}, _VKV'{k: \\\\\\\"meta\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"'{_VKV'{k: \\\\\\\\\\\\\\\"priority\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\\\\\\\\\\\\\"\\\\\\\\\\\\\\\"}}, _VKV'{k: \\\\\\\\\\\\\\\"labels\\\\\\\\\\\\\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"x\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"y\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}}\\\\\\\\\\\\\\\"}}}\\\\\\\"}}}\\\"}}\"}}}"}}
};
end
endmodule
