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
task process(input _VVal p0, input _VVal p1, input _VVal p2, input _VVal p3, input _VVal p4, input _VVal p5, input _VVal p6, input _VVal p7, input _VVal p8, input _VVal p9, input _VVal p10, input _VVal p11, input _VVal p12, input _VVal p13, input _VVal p14, input _VVal p15, input _VVal p16, input _VVal p17, input _VVal p18, input _VVal p19, input _VVal p20, input _VVal p21, input _VVal p22, input _VVal p23, input _VVal p24, input _VVal p25, input _VVal p26); endtask
initial begin
process(_VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 6, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 7, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 8, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 9, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 10, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 11, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 12, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 13, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 14, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 15, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 16, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 17, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 18, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 19, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 20, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 21, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 22, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 23, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 24, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 25, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 26, r: 0.0, s: ""});
end
endmodule
