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
    // before apple
    '{_VVAL_STR, 0, 0.0, "apple"},
    '{_VVAL_STR, 0, 0.0, "banana"}  // banana inline
    // trailing
};
my_data = '{
    // before apple
    '{_VVAL_STR, 0, 0.0, "apple"},
    '{_VVAL_STR, 0, 0.0, "banana"}  // banana inline
    // trailing
};
end
endmodule
