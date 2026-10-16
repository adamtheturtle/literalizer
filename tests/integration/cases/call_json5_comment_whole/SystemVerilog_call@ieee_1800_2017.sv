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
task f(input _VVal a); endtask
initial begin
// scalar heading
// second heading line
// scalar inline
// inline continuation
// scalar trailing
void'(f(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}));
end
endmodule
