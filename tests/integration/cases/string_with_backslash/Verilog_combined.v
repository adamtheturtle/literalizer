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
    '{_VVAL_STR, 0, 0.0, "C:\\path\\to\\file"},
    '{_VVAL_STR, 0, 0.0, "back\\\\slash"},
    '{_VVAL_STR, 0, 0.0, "hello \\\"world\\\""},
    '{_VVAL_STR, 0, 0.0, "path\\to \"# file"},
    '{_VVAL_STR, 0, 0.0, "trailing\\"},
    '{_VVAL_STR, 0, 0.0, "both \"quotes''' here"},
    '{_VVAL_STR, 0, 0.0, "line1\\nline2\nwith newline"}
};
my_data = '{
    '{_VVAL_STR, 0, 0.0, "C:\\path\\to\\file"},
    '{_VVAL_STR, 0, 0.0, "back\\\\slash"},
    '{_VVAL_STR, 0, 0.0, "hello \\\"world\\\""},
    '{_VVAL_STR, 0, 0.0, "path\\to \"# file"},
    '{_VVAL_STR, 0, 0.0, "trailing\\"},
    '{_VVAL_STR, 0, 0.0, "both \"quotes''' here"},
    '{_VVAL_STR, 0, 0.0, "line1\\nline2\nwith newline"}
};
end
endmodule
