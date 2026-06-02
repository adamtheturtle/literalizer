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
    _VKV'{k: "user_name", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "user.name", v: _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}},
    _VKV'{k: "user-name", v: _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}},
    _VKV'{k: "field_name_that_is_really_quite_long_one", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}},
    _VKV'{k: "field_name_that_is_really_quite_long_two", v: _VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""}}
};
my_data = '{
    _VKV'{k: "user_name", v: _VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}},
    _VKV'{k: "user.name", v: _VVal'{tag: _VVAL_INT, i: 2, r: 0.0, s: ""}},
    _VKV'{k: "user-name", v: _VVal'{tag: _VVAL_INT, i: 3, r: 0.0, s: ""}},
    _VKV'{k: "field_name_that_is_really_quite_long_one", v: _VVal'{tag: _VVAL_INT, i: 4, r: 0.0, s: ""}},
    _VKV'{k: "field_name_that_is_really_quite_long_two", v: _VVal'{tag: _VVAL_INT, i: 5, r: 0.0, s: ""}}
};
end
endmodule
