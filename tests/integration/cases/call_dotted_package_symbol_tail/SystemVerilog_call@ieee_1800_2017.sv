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
class HelperType_;
    task list(input _VVal a); endtask
endclass
HelperType_ helper = new();
initial begin
helper.list(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
