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
function _VVal make_widget();
    make_widget = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
endfunction
initial begin
static _VVal my_data = make_widget();
end
endmodule
