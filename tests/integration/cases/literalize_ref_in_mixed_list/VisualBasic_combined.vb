Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New Dictionary(Of String, Object) From {{"$ref", "ref_x"}},
            1,
            2
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New Dictionary(Of String, Object) From {{"$ref", "ref_x"}},
            1,
            2
        }
    End Sub
End Module
