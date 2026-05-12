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
    _VKV'{k: "omap_value", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"first\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "sibling_lists", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"numbers\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \\\"\\\"}}\"}}, _VKV'{k: \"strings\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"x\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"y\\\"}}\"}}}"}},
    _VKV'{k: "ref_marker_present", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"$keep\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"z\"}}"}}
};
my_data = '{
    _VKV'{k: "omap_value", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"first\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "sibling_lists", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"numbers\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \\\"\\\"}}\"}}, _VKV'{k: \"strings\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"x\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"y\\\"}}\"}}}"}},
    _VKV'{k: "ref_marker_present", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"$keep\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"z\"}}"}}
};
end
endmodule
