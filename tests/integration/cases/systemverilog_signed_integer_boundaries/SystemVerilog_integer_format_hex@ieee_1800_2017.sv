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
    _VKV'{k: "i32_below", v: _VVal'{tag: _VVAL_INT, i: -64'h80000001, r: 0.0, s: ""}},
    _VKV'{k: "i32_minimum", v: _VVal'{tag: _VVAL_INT, i: -64'h80000000, r: 0.0, s: ""}},
    _VKV'{k: "i32_above", v: _VVal'{tag: _VVAL_INT, i: -64'h7fffffff, r: 0.0, s: ""}},
    _VKV'{k: "i32_maximum", v: _VVal'{tag: _VVAL_INT, i: 64'h7fffffff, r: 0.0, s: ""}},
    _VKV'{k: "i32_over", v: _VVal'{tag: _VVAL_INT, i: 64'h80000000, r: 0.0, s: ""}},
    _VKV'{k: "i64_minimum", v: _VVal'{tag: _VVAL_INT, i: -64'h8000000000000000, r: 0.0, s: ""}},
    _VKV'{k: "i64_maximum", v: _VVal'{tag: _VVAL_INT, i: 64'h7fffffffffffffff, r: 0.0, s: ""}}
};
end
endmodule
