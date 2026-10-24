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
static _VKV std[] = '{
    _VKV'{k: "nan", v: _VVal'{tag: _VVAL_REAL, i: 0, r: $bitstoreal(64'h7FF8000000000000), s: ""}},
    _VKV'{k: "positive", v: _VVal'{tag: _VVAL_REAL, i: 0, r: $bitstoreal(64'h7FF0000000000000), s: ""}},
    _VKV'{k: "negative", v: _VVal'{tag: _VVAL_REAL, i: 0, r: $bitstoreal(64'hFFF0000000000000), s: ""}}
};
end
endmodule
