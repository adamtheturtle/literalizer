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
function _VVal record_entry(input _VVal s, input _VVal n, input _VVal b);
    record_entry = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
endfunction
initial begin
static _VVal my_data = record_entry(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "a"}, _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}, _VVal'{tag: _VVAL_BOOL, i: 1, r: 0.0, s: ""});
end
endmodule
