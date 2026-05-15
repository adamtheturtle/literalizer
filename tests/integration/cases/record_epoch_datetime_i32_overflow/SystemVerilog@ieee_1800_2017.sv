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
static _VKV my_data[] = '{
    _VKV'{k: "within_i32", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-01-15T12:00:00"}},
    _VKV'{k: "beyond_i32", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2099-06-15T08:30:00"}}
};
end
endmodule
