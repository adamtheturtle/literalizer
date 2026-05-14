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
    _VKV'{k: "id", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "description", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "example"}},
    _VKV'{k: "is_done", v: _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""}},
    _VKV'{k: "blocks", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}, _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}, _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: \"\"}}"}}
};
end
endmodule
