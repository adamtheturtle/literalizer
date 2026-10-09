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
static _VVal my_null = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
static _VVal regular_null = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
void'(consume(my_null));
void'(consume(regular_null));
end
endmodule
