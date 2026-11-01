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
    _VKV'{k: "ancient_date", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1500-03-01"}},
    _VKV'{k: "modern_date", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "2024-01-15"}},
    _VKV'{k: "before_date", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-04"}},
    _VKV'{k: "gap_date", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-10"}},
    _VKV'{k: "transition_date", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-15"}},
    _VKV'{k: "after_date", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-16"}},
    _VKV'{k: "before_naive", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-04T12:30:00.000001"}},
    _VKV'{k: "gap_naive", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-10T12:30:00.500000"}},
    _VKV'{k: "transition_positive", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-15T00:30:00+18:00"}},
    _VKV'{k: "transition_negative", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-15T23:30:00-18:00"}},
    _VKV'{k: "after_positive", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "1582-10-16T00:30:00+18:00"}}
};
end
endmodule
