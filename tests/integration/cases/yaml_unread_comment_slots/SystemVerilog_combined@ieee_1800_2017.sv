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
    _VKV'{k: "flow", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},\n        // After the first element.\n        _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}\n    }"}},
    // Between the key and its value.
    _VKV'{k: "gap", v: _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}},
    // On the block scalar header.
    _VKV'{k: "block", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Text.\n"}},
    _VKV'{k: "nested", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}\n        // On the nested alias.\n    }"}},
    _VKV'{k: "anchored", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}},
    _VKV'{k: "alias", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}}
    // On the alias.
};
my_data = '{
    _VKV'{k: "flow", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},\n        // After the first element.\n        _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}\n    }"}},
    // Between the key and its value.
    _VKV'{k: "gap", v: _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}},
    // On the block scalar header.
    _VKV'{k: "block", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Text.\n"}},
    _VKV'{k: "nested", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},\n        _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}\n        // On the nested alias.\n    }"}},
    _VKV'{k: "anchored", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}},
    _VKV'{k: "alias", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}}
    // On the alias.
};
end
endmodule
