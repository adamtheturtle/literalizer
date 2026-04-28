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
    _VKV'{k: "s", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "string"}},
    _VKV'{k: "i", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "f", v: _VVal'{tag: _VVAL_REAL, i: 0, r: 1.5, s: ""}},
    _VKV'{k: "b", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "n", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""}},
    _VKV'{k: "d", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-01-15"}},
    _VKV'{k: "dt", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-01-15T12:00:00"}},
    _VKV'{k: "by", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "48656c6c6f"}}
};
end
endmodule
