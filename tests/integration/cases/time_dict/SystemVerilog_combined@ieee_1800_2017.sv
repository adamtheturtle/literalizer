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
    _VKV'{k: "morning", v: "09:30:00"},
    _VKV'{k: "afternoon", v: "14:15:00"},
    _VKV'{k: "evening", v: "23:59:59"}
};
my_data = '{
    _VKV'{k: "morning", v: "09:30:00"},
    _VKV'{k: "afternoon", v: "14:15:00"},
    _VKV'{k: "evening", v: "23:59:59"}
};
end
endmodule
