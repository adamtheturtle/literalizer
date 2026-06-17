with A_Stub; use A_Stub;
procedure Main is
    procedure Put (Key : A_Val; Value : A_Val) is begin null; end Put;
    procedure Get (Key : A_Val) is begin null; end Get;
begin
    Put(key => AInt (1), value => AInt (10));
    Get(key => AInt (1));
end Main;
