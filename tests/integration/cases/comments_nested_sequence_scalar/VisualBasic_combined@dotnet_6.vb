Imports System.Collections.Generic
Module Check
    Sub _declaration()
        Dim my_data = New String()() {
            New String() {"ADD", "alice", "hello"},
            New String() {"DEL", "bob", "5"}
        }
    End Sub
    Sub _assignment()
        Dim my_data As Object
        my_data = New String()() {
            New String() {"ADD", "alice", "hello"},
            New String() {"DEL", "bob", "5"}
        }
    End Sub
End Module
