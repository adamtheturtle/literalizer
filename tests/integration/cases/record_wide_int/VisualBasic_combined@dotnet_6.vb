Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Dictionary(Of String, Object) From {
            {"quantity", 1000000},
            {"big", 18446744073709551615UL},
            {"ratio", 2.5},
            {"label", "tag"},
            {"ok", True}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Dictionary(Of String, Object) From {
            {"quantity", 1000000},
            {"big", 18446744073709551615UL},
            {"ratio", 2.5},
            {"label", "tag"},
            {"ok", True}
        }
    End Sub
End Module
