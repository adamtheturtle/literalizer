Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New Object() {
            New HashSet(Of Object)(),
            New HashSet(Of Integer) From {1, 2},
            New Object() {}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New Object() {
            New HashSet(Of Object)(),
            New HashSet(Of Integer) From {1, 2},
            New Object() {}
        }
    End Sub
End Module
