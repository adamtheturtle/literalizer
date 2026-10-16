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
// empty heading
// empty body
// after empty
static _VKV my_data[] = '{};
// empty heading
// empty body
// after empty
my_data = '{};
end
endmodule
