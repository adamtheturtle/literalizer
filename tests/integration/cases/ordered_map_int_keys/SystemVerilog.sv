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
    _VKV'{k: "1", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "one"}},
    _VKV'{k: "2", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "two"}},
    _VKV'{k: "42", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "answer"}}
};
end
endmodule
