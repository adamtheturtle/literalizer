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
    _VKV'{k: "exact_millisecond", v: "09:30:15.123000"},
    _VKV'{k: "sub_millisecond", v: "09:30:15.123456"}
};
my_data = '{
    _VKV'{k: "exact_millisecond", v: "09:30:15.123000"},
    _VKV'{k: "sub_millisecond", v: "09:30:15.123456"}
};
end
endmodule
