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
task f(input _VVal ops); endtask
initial begin
f(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"DEL\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"b\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"10\\\"}}\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"ADD\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"a\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"x\\\"}}\"}}"});  // note
end
endmodule
