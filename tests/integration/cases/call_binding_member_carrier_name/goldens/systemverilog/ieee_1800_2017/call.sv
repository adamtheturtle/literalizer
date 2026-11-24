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
class ObjType_;
    function _VVal ZVal(input _VVal _arg);
        ZVal = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
    endfunction
endclass
ObjType_ obj = new();
initial begin
static _VVal my_data = obj.ZVal(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}); // note
end
endmodule
