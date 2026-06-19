with A_Stub; use A_Stub;
procedure Main is
    procedure Store_Item (Key : A_Val; Value : A_Val) is begin null; end Store_Item;
    procedure Read_Item (Key : A_Val) is begin null; end Read_Item;
begin
    Store_Item(key => AInt (1), value => AInt (10));
    Read_Item(key => AInt (1));
end Main;
