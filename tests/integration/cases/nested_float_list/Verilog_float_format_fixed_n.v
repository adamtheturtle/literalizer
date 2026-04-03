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
    '{'{_VVAL_REAL, 0, 1.500000, ""}, '{_VVAL_REAL, 0, 2.500000, ""}},
    '{'{_VVAL_REAL, 0, 3.500000, ""}, '{_VVAL_REAL, 0, 4.500000, ""}}
};
end
endmodule
