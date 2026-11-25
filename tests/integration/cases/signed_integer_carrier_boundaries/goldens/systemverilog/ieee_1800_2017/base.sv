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
    _VKV'{k: "i32_below", v: _VVal'{tag: _VVAL_INT, i: -64'sd2147483649, r: 0.0, s: ""}},
    _VKV'{k: "i32_minimum", v: _VVal'{tag: _VVAL_INT, i: -64'sd2147483648, r: 0.0, s: ""}},
    _VKV'{k: "i32_above", v: _VVal'{tag: _VVAL_INT, i: -2147483647, r: 0.0, s: ""}},
    _VKV'{k: "i32_maximum", v: _VVal'{tag: _VVAL_INT, i: 2147483647, r: 0.0, s: ""}},
    _VKV'{k: "i32_over", v: _VVal'{tag: _VVAL_INT, i: 64'sd2147483648, r: 0.0, s: ""}},
    _VKV'{k: "i64_minimum", v: _VVal'{tag: _VVAL_INT, i: -64'sd9223372036854775808, r: 0.0, s: ""}},
    _VKV'{k: "i64_maximum", v: _VVal'{tag: _VVAL_INT, i: 64'sd9223372036854775807, r: 0.0, s: ""}}
};
end
endmodule
