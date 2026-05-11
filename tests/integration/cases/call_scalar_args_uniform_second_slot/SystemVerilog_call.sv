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
task process(input _VVal value, input _VVal label); endtask
initial begin
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "a"});
process(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "b"});
process(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "c"});
end
endmodule
