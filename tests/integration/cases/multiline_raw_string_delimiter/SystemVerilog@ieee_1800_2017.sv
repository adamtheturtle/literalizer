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
initial begin
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "custom base after empty collision: )\"\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "custom suffix after base collision: )\" and )x0\"\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "custom second suffix: )\" and )x0\" and )x00\"\nvalue"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "long base exhaustion: )\" and )abcdefghijklmnop\"\nvalue"}
};
end
endmodule
