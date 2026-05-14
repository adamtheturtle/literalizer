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
    _VKV'{k: "first", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "one"}},
    _VKV'{k: "second", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "two"}},
    _VKV'{k: "third", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "three"}}
};
my_data = '{
    _VKV'{k: "first", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "one"}},
    _VKV'{k: "second", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "two"}},
    _VKV'{k: "third", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "three"}}
};
end
endmodule
