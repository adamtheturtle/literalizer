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
    // About the first dotted key.
    // About the second dotted key.
    _VKV'{k: "dotted", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"first\", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: \"\"}}, _VKV'{k: \"second\", v: _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: \"\"}}}"}},
    _VKV'{k: "plain", v: _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}},  // About the plain key.
    // Before the first entry.
    // Before the second entry.
    _VKV'{k: "entries", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"name\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"one\\\"}}}\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"name\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"two\\\"}}}\"}}"}},
    // Inside the table.
    _VKV'{k: "table", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VKV'{k: \"inner\", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: \"\"}}}"}}
};
end
endmodule
