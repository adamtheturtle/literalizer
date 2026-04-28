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
    _VKV'{k: "key", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value \" # not a comment"}}  // real
};
my_data = '{
    _VKV'{k: "key", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "value \" # not a comment"}}  // real
};
end
endmodule
