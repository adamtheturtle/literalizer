with A_Stub; use A_Stub;
procedure Main is
    function Go (Value : A_Val) return A_Val is (ANull);
    item : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    declare
        Discarded_Value : constant A_Val := Go(value => item);
        pragma Unreferenced (Discarded_Value);
    begin
        null;
    end;
end Main;
