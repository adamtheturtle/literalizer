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
static _VKV val_x[] = '{
    _VKV'{k: "_", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "_"}}
};
static _VKV val_y[] = '{
    _VKV'{k: "_", v: _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "_"}}
};
static _VVal my_data[] = '{
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "val_x"},
    _VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "val_y"}
};
end
endmodule
