Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a_b", 1},
            {"a-b", 2},
            {"averyveryverylongkeynamethatgoesonandonandon", 3},
            {"averyveryverylongkeynamethatgoesonandmore", 4}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"a_b", 1},
            {"a-b", 2},
            {"averyveryverylongkeynamethatgoesonandonandon", 3},
            {"averyveryverylongkeynamethatgoesonandmore", 4}
        }
    End Sub
End Module
