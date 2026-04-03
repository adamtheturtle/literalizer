typedef enum {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
module check;
initial begin
_VVal my_data = '{
    '{_VVAL_INT, 0xf4240, 0.0, ""},
    '{_VVAL_INT, -0x4d2, 0.0, ""},
    '{_VVAL_INT, 0xff, 0.0, ""},
    '{_VVAL_INT, -0xa, 0.0, ""}
};
end
endmodule
