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
class MgrType_;
    task run(input _VVal operation); endtask
endclass
class AppType_;
    MgrType_ mgr = new();
endclass
AppType_ app = new();
initial begin
app.mgr.run(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"type\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"create\"}}, _VKV'{k: \"pr_id\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"pr_1\"}}, _VKV'{k: \"draft\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}}"});
app.mgr.run(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"type\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"create\"}}, _VKV'{k: \"pr_id\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"pr_2\"}}}"});
end
endmodule
