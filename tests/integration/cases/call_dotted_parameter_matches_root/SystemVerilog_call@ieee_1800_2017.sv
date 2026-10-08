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
class OuterType_;
    task inner(input _VVal outer, input _VVal n); endtask
endclass
OuterType_ outer = new();
initial begin
outer.inner(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""});
end
endmodule
