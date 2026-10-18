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
initial begin
static _VVal ref_data = _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""};
static _VKV my_data[] = ref_data;
end
endmodule
