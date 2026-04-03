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
    '{"x", '{_VVAL_INT, 1, 0.0, ""}, "y", '{_VVAL_REAL, 0, 2.5, ""}},
    '{"x", '{_VVAL_INT, 3, 0.0, ""}, "y", '{_VVAL_REAL, 0, 4.0, ""}}
};
end
endmodule
