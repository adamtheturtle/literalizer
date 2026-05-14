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
    _VKV'{k: "metrics", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"count\", v: _VVal'{tag: _VVAL_INT, i: 100, r: 0.0, s: \"\"}}, _VKV'{k: \"rate\", v: _VVal'{tag: _VVAL_INT, i: 50, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "flags", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"retries\", v: _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: \"\"}}, _VKV'{k: \"timeout\", v: _VVal'{tag: _VVAL_INT, i: 30, r: 0.0, s: \"\"}}}"}}
};
end
endmodule
