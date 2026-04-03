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
    '{_VVAL_STR, 0, 0.0, "foo"},
    '{_VVAL_STR, 0, 0.0, "bar"},
    '{_VVAL_STR, 0, 0.0, "baz"}
};
end
endmodule
