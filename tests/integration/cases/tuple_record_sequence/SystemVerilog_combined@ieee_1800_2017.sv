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
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"call\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"send\"}}, _VKV'{k: \"args\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"email\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"a@gmail.com\\\"}, _VVal'{tag: _VVAL_INT, i: 100, r: 0.0, s: \\\"\\\"}}\"}}}"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"call\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"recv\"}}, _VKV'{k: \"args\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"sms\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"b@example.com\\\"}, _VVal'{tag: _VVAL_INT, i: 200, r: 0.0, s: \\\"\\\"}}\"}}}"}
};
my_data = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"call\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"send\"}}, _VKV'{k: \"args\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"email\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"a@gmail.com\\\"}, _VVal'{tag: _VVAL_INT, i: 100, r: 0.0, s: \\\"\\\"}}\"}}}"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"call\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"recv\"}}, _VKV'{k: \"args\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \\\"\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"sms\\\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"b@example.com\\\"}, _VVal'{tag: _VVAL_INT, i: 200, r: 0.0, s: \\\"\\\"}}\"}}}"}
};
end
endmodule
