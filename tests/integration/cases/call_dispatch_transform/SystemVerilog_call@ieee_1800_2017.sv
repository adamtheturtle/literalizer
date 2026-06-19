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
function _VVal record_value(input _VVal value);
    record_value = _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""};
endfunction
task flush_buffer(input _VVal count); endtask
task emit(input _VVal _arg); endtask
initial begin
emit(record_value(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}));
flush_buffer(_VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""});
end
endmodule
