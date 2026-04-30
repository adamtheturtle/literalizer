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
static _VVal repeated_var = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
static _VVal single_var[] = '{
    _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 6, r: 0.0, s: ""}
};
process(repeated_var, _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
process(single_var, _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""});
process(repeated_var, _VVal'{tag: _VVAL_INT, i: 8, r: 0.0, s: ""});
end
endmodule
