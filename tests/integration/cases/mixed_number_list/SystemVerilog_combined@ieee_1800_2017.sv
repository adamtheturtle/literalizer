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
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 2.5, s: ""},
    _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}
};
my_data = '{
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""},
    _VVal'{tag: _VVAL_REAL, i: 0, r: 2.5, s: ""},
    _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}
};
end
endmodule
