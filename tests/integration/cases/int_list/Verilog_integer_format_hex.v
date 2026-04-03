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
    '{_VVAL_INT, 0x1, 0.0, ""},
    '{_VVAL_INT, 0x2, 0.0, ""},
    '{_VVAL_INT, 0x3, 0.0, ""}
};
end
endmodule
