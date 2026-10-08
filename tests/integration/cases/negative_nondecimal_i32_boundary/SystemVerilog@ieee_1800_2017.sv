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
    _VKV'{k: "minimum", v: _VVal'{tag: _VVAL_INT, i: -2147483648, r: 0.0, s: ""}},
    _VKV'{k: "below", v: _VVal'{tag: _VVAL_INT, i: -64'sd3000000000, r: 0.0, s: ""}}
};
end
endmodule
