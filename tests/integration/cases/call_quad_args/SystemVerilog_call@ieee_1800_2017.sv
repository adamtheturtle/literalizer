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
task process(input _VVal a, input _VVal b, input _VVal c, input _VVal d); endtask
initial begin
process(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""});
process(_VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 6, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 7, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 8, r: 0.0, s: ""});
end
endmodule
