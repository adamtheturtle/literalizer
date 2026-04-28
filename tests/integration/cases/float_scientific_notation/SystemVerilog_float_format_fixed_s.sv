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
    _VVal'{tag: _VVAL_REAL, i: 0, r: 0.000000, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 1.000000, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 1500.000000, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 0.001000, s: ""}
};
end
endmodule
