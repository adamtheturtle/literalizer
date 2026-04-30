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
task process(input _VVal data); endtask
initial begin
static _VVal my_var = _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""};
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"ref\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"myVar\\\"}}}\"}, _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: \"\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"static\"}}"});
end
endmodule
