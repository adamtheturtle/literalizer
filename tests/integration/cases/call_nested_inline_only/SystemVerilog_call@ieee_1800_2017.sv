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
task f(input _VVal a, input _VVal b); endtask
initial begin
f(_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"});  // trailing note
f(_VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "world"});  // another note
end
endmodule
