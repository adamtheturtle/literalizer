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
static _VVal empty_values[] = '{};
static _VVal integer_values[] = '{
    _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}
};
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "empty_values"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "integer_values"}
};
end
endmodule
