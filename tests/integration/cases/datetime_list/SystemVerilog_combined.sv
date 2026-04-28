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
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-01-15T12:30:00.123456+00:00"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-06-01T08:00:00+00:00"}
};
my_data = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-01-15T12:30:00.123456+00:00"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-06-01T08:00:00+00:00"}
};
end
endmodule
