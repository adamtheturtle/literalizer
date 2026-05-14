typedef enum int {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;
typedef struct {
    _VTag tag;
    longint i;
    real r;
    string s;
} _VVal;
typedef struct {
    string k;
    _VVal v;
} _VKV;
module main;
class ClientType_;
    task post(input _VVal data); endtask
endclass
class ApiType_;
    ClientType_ client = new();
endclass
class ObjType_;
    ApiType_ api = new();
endclass
ObjType_ obj = new();
initial begin
obj.api.client.post(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"});
obj.api.client.post(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""});
obj.api.client.post(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
