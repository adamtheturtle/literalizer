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
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"id\", v: _VVal'{tag: _VVAL_INT, i: 100, r: 0.0, s: \"\"}}, _VKV'{k: \"label\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"first entry\"}}, _VKV'{k: \"enabled\", v: _VVal'{tag: _VVAL_INT, i: 0, r: 0.0, s: \"\"}}, _VKV'{k: \"related_ids\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 102, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_INT, i: 103, r: 0.0, s: \\\"\\\"}}\"}}}"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"id\", v: _VVal'{tag: _VVAL_INT, i: 101, r: 0.0, s: \"\"}}, _VKV'{k: \"label\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"second entry\"}}, _VKV'{k: \"enabled\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}, _VKV'{k: \"related_ids\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 100, r: 0.0, s: \\\"\\\"}}\"}}}"}
};
end
endmodule
