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
task process(input _VVal value, input _VVal count); endtask
initial begin
process(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""});
process(_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 100, r: 0.0, s: ""});
end
endmodule
