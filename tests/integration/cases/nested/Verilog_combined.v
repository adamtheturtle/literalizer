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
    "users", '{'{"name", '{_VVAL_STR, 0, 0.0, "Bob"}, "tags", '{'{_VVAL_STR, 0, 0.0, "admin"}, '{_VVAL_STR, 0, 0.0, "user"}}}, '{"name", '{_VVAL_STR, 0, 0.0, "Carol"}, "tags", '{'{_VVAL_STR, 0, 0.0, "guest"}}}}
};
my_data = '{
    "users", '{'{"name", '{_VVAL_STR, 0, 0.0, "Bob"}, "tags", '{'{_VVAL_STR, 0, 0.0, "admin"}, '{_VVAL_STR, 0, 0.0, "user"}}}, '{"name", '{_VVAL_STR, 0, 0.0, "Carol"}, "tags", '{'{_VVAL_STR, 0, 0.0, "guest"}}}}
};
end
endmodule
