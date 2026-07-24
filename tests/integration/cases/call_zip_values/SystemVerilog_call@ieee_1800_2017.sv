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
function _VVal process(input _VVal value);
    process = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
endfunction
task emit(input _VVal _call, input _VVal _zip); endtask
initial begin
emit(process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"}), 1);
emit(process(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}), 0);
end
endmodule
