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
static _VVal my_var[] = '{
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}
};
static _VVal my_other[] = '{
    _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 6, r: 0.0, s: ""}
};
process(my_var, _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""});
process(my_other, _VVal'{tag: _VVAL_INT, i: 7, r: 0.0, s: ""});
end
endmodule
