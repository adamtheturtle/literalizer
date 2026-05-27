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
    _VVal'{tag: _VVAL_REAL, i: 0, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 1.0, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 1500.0, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 0.001, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 1e16, s: ""}
};
end
endmodule
