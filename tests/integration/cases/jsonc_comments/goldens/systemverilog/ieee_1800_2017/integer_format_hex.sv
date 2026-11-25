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
    // A JSONC input case with both comment forms.
    _VKV'{k: "url", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "https://example.org/a/*b*/"}},  // detail
    // continued
    _VKV'{k: "count", v: _VVal'{tag: _VVAL_INT, i: 64'h2, r: 0.0, s: ""}}  // trailing line comment
};
end
endmodule
