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
task process(input _VVal value, input _VVal count); endtask
initial begin
static _VVal my_int = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
static _VVal my_bool = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
static _VVal my_float = _VVal'{tag: _VVAL_REAL, i: 0, r: 3.14, s: ""};
static _VVal my_list[] = '{
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}
};
process(my_int, _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""});
process(my_bool, _VVal'{tag: _VVAL_INT, i: 7, r: 0.0, s: ""});
process(my_float, _VVal'{tag: _VVAL_INT, i: 9, r: 0.0, s: ""});
process(my_list, _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
