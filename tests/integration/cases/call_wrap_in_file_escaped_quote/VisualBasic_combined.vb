Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String()() {
            New String() {"a""b"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String()() {
            New String() {"a""b"}
        }
    End Sub
End Module
