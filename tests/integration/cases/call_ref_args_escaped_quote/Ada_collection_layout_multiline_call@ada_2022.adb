with A_Stub; use A_Stub;
procedure Main is
    procedure Process (V : A_Val) is begin null; end Process;
    my_str : A_Val := AStr ("a""b");
begin
    Process(v => my_str);
end Main;
