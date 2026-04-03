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
    '{_VVAL_REAL, 0, $bitstoreal(64'h7FF0000000000000), ""},
    '{_VVAL_REAL, 0, $bitstoreal(64'hFFF0000000000000), ""},
    '{_VVAL_REAL, 0, $bitstoreal(64'h7FF8000000000000), ""}
};
end
endmodule
