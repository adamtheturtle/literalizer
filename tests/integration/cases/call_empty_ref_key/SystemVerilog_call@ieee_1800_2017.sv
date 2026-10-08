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
task consume(input _VVal value); endtask
initial begin
static _VVal external_value = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
consume(external_value);
end
endmodule
