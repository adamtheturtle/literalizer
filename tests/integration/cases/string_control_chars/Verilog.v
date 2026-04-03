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
    '{_VVAL_STR, 0, 0.0, "line1\r\nline2"},
    '{_VVAL_STR, 0, 0.0, "line1\rline2"},
    '{_VVAL_STR, 0, 0.0, ""}
};
end
endmodule
