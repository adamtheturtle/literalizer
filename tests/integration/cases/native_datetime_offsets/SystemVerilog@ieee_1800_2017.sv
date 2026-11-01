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
static _VKV my_data[] = '{
    _VKV'{k: "stamps", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"2001-02-03T04:05:06+00:00:01\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"2001-02-03T04:05:06-00:00:01\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"2001-02-03T04:05:06+00:00:00.000001\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"2001-02-03T04:05:06-00:00:00.000001\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"2001-02-03T04:05:06+05:30:15.000001\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"2001-02-03T04:05:06-05:30:15.000001\"}}"}}
};
end
endmodule
