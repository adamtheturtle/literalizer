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
task f(input _VVal value); endtask
initial begin
static _VVal ref_data[] = '{
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}
};
void'(f(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"ref_data\"}\n}"}));
void'(f(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"ref_data\"}\n}"}));
end
endmodule
