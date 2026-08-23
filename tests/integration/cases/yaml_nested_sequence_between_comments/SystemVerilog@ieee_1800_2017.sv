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
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"item\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"existing\\\"}}}\"},\n        _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"kept\"}\n        // This comment trails the first pair.\n    }"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"item\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"next\\\"}}}\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"also kept\"}}"},
    // This comment describes the last pair.
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{_VKV'{k: \\\"item\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"last\\\"}}}\"}, _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"kept too\"}}"}
};
end
endmodule
