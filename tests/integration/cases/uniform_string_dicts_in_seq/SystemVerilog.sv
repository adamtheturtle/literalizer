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
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"first\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"Alice\"}}, _VKV'{k: \"last\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"Smith\"}}}"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"first\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"Bob\"}}, _VKV'{k: \"last\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"Jones\"}}}"}
};
end
endmodule
