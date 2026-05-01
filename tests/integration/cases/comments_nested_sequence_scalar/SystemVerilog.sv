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
initial begin
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"ADD\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"alice\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"hello\"}}"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"DEL\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"bob\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"5\"}}"}  // removes "world"
};
end
endmodule
