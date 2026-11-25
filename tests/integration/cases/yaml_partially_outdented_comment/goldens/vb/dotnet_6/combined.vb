Imports System.Collections.Generic
Module Check
    Sub _declaration()
        ' Outdented from the inner mapping too, so the root claims this.
        Dim my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {{"b", New Integer() {1}}, {"c", 2}}},
            {"d", 3}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        ' Outdented from the inner mapping too, so the root claims this.
        my_data = New Dictionary(Of String, Object) From {
            {"a", New Dictionary(Of String, Object) From {{"b", New Integer() {1}}, {"c", 2}}},
            {"d", 3}
        }
    End Sub
End Module
