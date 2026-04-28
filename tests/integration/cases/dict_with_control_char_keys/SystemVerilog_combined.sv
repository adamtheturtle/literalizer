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
    _VKV'{k: "key\nwith\nnewlines", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value1"}},
    _VKV'{k: "key\twith\ttabs", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value2"}},
    _VKV'{k: "", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value3"}}
};
my_data = '{
    _VKV'{k: "key\nwith\nnewlines", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value1"}},
    _VKV'{k: "key\twith\ttabs", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value2"}},
    _VKV'{k: "", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value3"}}
};
end
endmodule
