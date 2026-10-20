with A_Stub; use A_Stub;
procedure Main is
    procedure Process (Data : A_Val) is begin null; end Process;
    item : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    Process(data => AList'[item, item]);
end Main;
