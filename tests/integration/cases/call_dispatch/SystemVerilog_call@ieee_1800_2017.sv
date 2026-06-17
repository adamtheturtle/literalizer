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
task put(input _VVal key, input _VVal value); endtask
task get(input _VVal key); endtask
initial begin
put(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 10, r: 0.0, s: ""});
get(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
