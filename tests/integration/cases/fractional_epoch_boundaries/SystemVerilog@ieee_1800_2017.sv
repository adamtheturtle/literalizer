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
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1970-01-01T00:00:00.000001+00:00"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1969-12-31T23:59:59.500000+00:00"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1970-01-01T00:00:01+00:00"}
};
end
endmodule
