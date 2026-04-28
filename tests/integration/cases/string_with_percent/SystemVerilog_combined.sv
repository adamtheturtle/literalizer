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
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "100% done"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "%(name) is here"}
};
my_data = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "100% done"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "%(name) is here"}
};
end
endmodule
