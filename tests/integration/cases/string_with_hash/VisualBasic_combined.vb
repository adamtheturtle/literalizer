Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String() {
            "issue #{42}",
            "color #red"
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String() {
            "issue #{42}",
            "color #red"
        }
    End Sub
End Module
