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
class TracerType_;
    task emit(input _VVal _arg); endtask
endclass
TracerType_ tracer = new();
initial begin
tracer.emit(process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"}));
tracer.emit(process(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}));
tracer.emit(process(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}));
end
endmodule
