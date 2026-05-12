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
    _VKV'{k: "users", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "'{\n        _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{\\n            _VKV'{k: \\\"name\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"Bob\\\"}},\\n            _VKV'{k: \\\"tags\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{\\\\n                _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"admin\\\\\\\"},\\\\n                _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"user\\\\\\\"}\\\\n            }\\\"}}\\n        }\"},\n        _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \"'{\\n            _VKV'{k: \\\"name\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"Carol\\\"}},\\n            _VKV'{k: \\\"tags\\\", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\"'{\\\\n                _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: \\\\\\\"guest\\\\\\\"}\\\\n            }\\\"}}\\n        }\"}\n    }"}}
};
end
endmodule
