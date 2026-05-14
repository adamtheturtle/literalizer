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
task process(input _VVal value); endtask
initial begin
// Test cases
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"type\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"create\"}}, _VKV'{k: \"pr_id\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"pr_1\"}}}"});  // first case
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"type\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"update\"}}, _VKV'{k: \"pr_id\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"pr_2\"}}}"});  // second case
// third case
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"type\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"delete\"}}, _VKV'{k: \"pr_id\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"pr_3\"}}}"});
end
endmodule
