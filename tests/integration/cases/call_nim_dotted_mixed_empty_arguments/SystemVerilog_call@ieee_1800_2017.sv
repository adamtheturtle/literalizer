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
    function _VVal go(input _VVal before, input _VVal populated, input _VVal after);
        go = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
    endfunction
endclass
ThingType_ thing = new();
initial begin
void'(thing.go(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{}"}));
void'(thing.go(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"text\"}}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{}"}));
void'(thing.go(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"text\"}}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{}"}));
void'(thing.go(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"text\"}}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: \"\"}}"}));
end
endmodule
