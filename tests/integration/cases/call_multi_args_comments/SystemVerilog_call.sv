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
task process(input _VVal ts, input _VVal start, input _VVal end); endtask
initial begin
process(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 3600, r: 0.0, s: ""});  // Jan 1 1970 00:00:00 - 01:00:00
process(_VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 3600, r: 0.0, s: ""});  // Jan 1 1970 00:00:05 - 01:00:05
process(_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""}, _VVal'{tag: _VVAL_INT, i: 5400, r: 0.0, s: ""});  // Jan 1 1970 00:00:02 - 01:30:02
end
endmodule
