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
task process(input _VVal data, input _VVal count); endtask
initial begin
static _VVal shared = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
static _VVal other = _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""};
process(shared, _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
process(other, _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""});
process(shared, _VVal'{tag: _VVAL_INT, i: 8, r: 0.0, s: ""});
end
endmodule
