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
    _VKV'{k: "if", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "then", v: _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}},
    _VKV'{k: "else", v: _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}},
    _VKV'{k: "let", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}},
    _VKV'{k: "in", v: _VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""}},
    _VKV'{k: "using", v: _VVal'{tag: _VVAL_INT, i: 6, r: 0.0, s: ""}},
    _VKV'{k: "missing", v: _VVal'{tag: _VVAL_INT, i: 7, r: 0.0, s: ""}},
    _VKV'{k: "assert", v: _VVal'{tag: _VVAL_INT, i: 8, r: 0.0, s: ""}},
    _VKV'{k: "as", v: _VVal'{tag: _VVAL_INT, i: 9, r: 0.0, s: ""}},
    _VKV'{k: "Infinity", v: _VVal'{tag: _VVAL_INT, i: 10, r: 0.0, s: ""}},
    _VKV'{k: "NaN", v: _VVal'{tag: _VVAL_INT, i: 11, r: 0.0, s: ""}},
    _VKV'{k: "merge", v: _VVal'{tag: _VVAL_INT, i: 12, r: 0.0, s: ""}},
    _VKV'{k: "Some", v: _VVal'{tag: _VVAL_INT, i: 13, r: 0.0, s: ""}},
    _VKV'{k: "toMap", v: _VVal'{tag: _VVAL_INT, i: 14, r: 0.0, s: ""}},
    _VKV'{k: "forall", v: _VVal'{tag: _VVAL_INT, i: 15, r: 0.0, s: ""}},
    _VKV'{k: "with", v: _VVal'{tag: _VVAL_INT, i: 16, r: 0.0, s: ""}},
    _VKV'{k: "ordinary", v: _VVal'{tag: _VVAL_INT, i: 17, r: 0.0, s: ""}}
};
end
endmodule
