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
static _VVal x = _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""};
static _VVal y = _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""};
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "x"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "y"}
};
end
endmodule
