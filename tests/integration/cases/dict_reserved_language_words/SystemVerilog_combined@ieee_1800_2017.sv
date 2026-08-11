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
    _VKV'{k: "assert", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "else", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "error", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "false", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "for", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "function", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "if", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "import", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "importbin", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "importstr", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "in", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "local", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "null", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "self", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "super", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "tailstrict", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "then", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "true", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "ordinary", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}}
};
my_data = '{
    _VKV'{k: "assert", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "else", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "error", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "false", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "for", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "function", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "if", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "import", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "importbin", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "importstr", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "in", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "local", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "null", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "self", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "super", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "tailstrict", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "then", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "true", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "ordinary", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}}
};
end
endmodule
