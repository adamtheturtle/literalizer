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
initial begin
function _VVal make_widget(input _VVal count);
    make_widget = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
endfunction
static _VVal result = _VVal'{tag: _VVAL_INT, i: make_widget(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}), r: 0.0, s: ""};
end
endmodule
