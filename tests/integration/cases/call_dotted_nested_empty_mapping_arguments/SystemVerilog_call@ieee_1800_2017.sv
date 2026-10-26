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
class WorkerType_;
    task process(input _VVal values, input _VVal count); endtask
endclass
class ApiType_;
    WorkerType_ worker = new();
endclass
ApiType_ api = new();
initial begin
void'(api.worker.process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{}\"}}"}, _VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""}));
void'(api.worker.process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"x\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"s\\\"}}}\"}}"}, _VVal'{tag: _VVAL_INT, i: 43, r: 0.0, s: ""}));
end
endmodule
