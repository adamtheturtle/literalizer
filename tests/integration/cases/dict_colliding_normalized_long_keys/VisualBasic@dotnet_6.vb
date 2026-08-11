Imports System.Collections.Generic
Module Check
    Dim my_data = New Dictionary(Of String, Object) From {
        {"a_b", 1},
        {"a-b", 2},
        {"averyveryverylongkeynamethatgoesonandonandon", 3},
        {"averyveryverylongkeynamethatgoesonandmore", 4}
    }
End Module
