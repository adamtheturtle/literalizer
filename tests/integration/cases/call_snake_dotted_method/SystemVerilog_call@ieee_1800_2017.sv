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
class Http_ClientType_;
    task fetch(input _VVal payload); endtask
endclass
class My_AppType_;
    Http_ClientType_ http_client = new();
endclass
My_AppType_ my_app = new();
initial begin
my_app.http_client.fetch(_VVal'{tag: _VVAL_STR, i: 0, r: 0.0, s: "hello"});
my_app.http_client.fetch(_VVal'{tag: _VVAL_INT, i: 42, r: 0.0, s: ""});
my_app.http_client.fetch(_VVal'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""});
end
endmodule
