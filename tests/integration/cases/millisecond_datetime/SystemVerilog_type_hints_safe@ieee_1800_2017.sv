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
    _VKV'{k: "half", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1979-05-27T07:32:00.500000"}},
    _VKV'{k: "milli", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1979-05-27T07:32:00.100000"}},
    _VKV'{k: "max_milli", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1979-05-27T07:32:00.999000"}},
    _VKV'{k: "whole", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1979-05-27T07:32:00"}}
};
end
endmodule
