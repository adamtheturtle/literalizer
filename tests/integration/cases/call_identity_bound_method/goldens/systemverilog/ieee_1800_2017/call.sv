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
class ThingType_;
    function _VVal go(input _VVal value);
        go = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
    endfunction
endclass
ThingType_ thing = new();
initial begin
static _VVal item[] = '{
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}
};
void'(thing.go(item));
end
endmodule
