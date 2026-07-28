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
task process(input _VVal known_value, input _VVal nested_missing); endtask
initial begin
static _VVal known_value = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
static _VVal unknown_value = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
process(known_value, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"unknown_value\"}}"});
end
endmodule
