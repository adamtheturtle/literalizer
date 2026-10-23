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
    _VKV'{k: "comma_hash", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "a,#b"}},
    _VKV'{k: "comma_space_hash", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "trail, # comment"}},
    _VKV'{k: "escaped_quote", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "quote \" and , #"}},
    _VKV'{k: "next_line", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "xy"}},
    _VKV'{k: "line_separator", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "x y"}},
    _VKV'{k: "paragraph_separator", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "x y"}}
};
end
endmodule
