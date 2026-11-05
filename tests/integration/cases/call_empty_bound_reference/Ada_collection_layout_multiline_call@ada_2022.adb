with A_Stub; use A_Stub;
procedure Main is
    function Make_Widget (Value : A_Val) return A_Val is (ANull);
    items : A_Val := AList'[];
begin
    declare
        Discarded_Value : constant A_Val := Make_Widget(value => items);
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
end Main;
