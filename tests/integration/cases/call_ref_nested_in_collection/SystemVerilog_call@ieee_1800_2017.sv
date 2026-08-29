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
task process(input _VVal a, input _VVal b); endtask
initial begin
static _VVal big_list[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "x"}
};
process(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"k\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"big_list\"}}}"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"m\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"big_list\"}}}"});
end
endmodule
