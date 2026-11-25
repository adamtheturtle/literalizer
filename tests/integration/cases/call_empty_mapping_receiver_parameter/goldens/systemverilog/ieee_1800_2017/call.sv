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
class ApiType_;
    task process(input _VVal self); endtask
endclass
ApiType_ api = new();
initial begin
void'(api.process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{}"}));
end
endmodule
