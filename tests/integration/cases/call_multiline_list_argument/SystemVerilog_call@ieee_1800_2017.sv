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
task process(input _VVal xs); endtask
initial begin
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"},\n    _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}\n}"});
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n    _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: \"\"}\n}"});
end
endmodule
