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
task consume(input _VVal items, input _VVal mapping); endtask
initial begin
static _VVal foo = _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""};
consume(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{\\n        _VKV'{k: \\\"other\\\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}}\\n    }\"},\n    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"foo\"}\n}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n    _VKV'{k: \"left\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"foo\"}},\n    _VKV'{k: \"other\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}\n}"});
end
endmodule
