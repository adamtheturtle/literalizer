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
    _VKV'{k: "a", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        // inner note\n        _VKV'{k: \"b\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}  // inline b\n    }"}},
    _VKV'{k: "list", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},  // first\n        _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}  // second\n    }"}}
};
my_data = '{
    _VKV'{k: "a", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        // inner note\n        _VKV'{k: \"b\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}  // inline b\n    }"}},
    _VKV'{k: "list", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},  // first\n        _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}  // second\n    }"}}
};
end
endmodule
