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
task process(input _VVal value); endtask
initial begin
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Dune"});  // first edition
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Solaris"});
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "Neuromancer"});  // cyberpunk
end
endmodule
