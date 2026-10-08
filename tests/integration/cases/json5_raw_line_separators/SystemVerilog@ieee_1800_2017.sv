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
    _VKV'{k: "double", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "a b"}},
    _VKV'{k: "single", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "c d"}},
    _VKV'{k: "both", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "e f g"}},
    _VKV'{k: "continued", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hi"}},
    _VKV'{k: "escaped backslash", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "j\\ k"}}
};
end
endmodule
