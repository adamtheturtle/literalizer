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
static _VVal my_data[] = '{
    // strings stay data
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "https://example.org/a/*b*/"},  // URL annotation
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "escaped quote: \" // still data"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "backslash: \\"},  // outside the string
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "/* not a comment */"}
};
end
endmodule
