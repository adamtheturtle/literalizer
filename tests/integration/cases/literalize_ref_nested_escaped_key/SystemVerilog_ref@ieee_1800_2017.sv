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
static _VKV foo[] = '{
    _VKV'{k: "_", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "_"}}
};
static _VKV my_data[] = '{
    _VKV'{k: "items", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"other\\\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}}}\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"foo\"}}"}},
    _VKV'{k: "mapping", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"value\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"foo\"}}}"}}
};
end
endmodule
