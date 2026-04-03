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
    '{_VVAL_STR, 0, 0.0, "2024-01-15T12:30:00.123456+00:00"},
    '{_VVAL_STR, 0, 0.0, "2024-06-01T08:00:00+00:00"}
};
my_data = '{
    '{_VVAL_STR, 0, 0.0, "2024-01-15T12:30:00.123456+00:00"},
    '{_VVAL_STR, 0, 0.0, "2024-06-01T08:00:00+00:00"}
};
end
endmodule
