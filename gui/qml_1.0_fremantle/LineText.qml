//LineText.qml
import Qt 4.7
import QtQuick 1.0
import org.maemo.fremantle 1.0

Item {
    id: lineTextMain

    height: label.height

    property alias text: label.text

    Rectangle {
        id: line
        color : "black"
        height : 2

        anchors {
            left: parent.left
            right : label.left
            verticalCenter: parent.verticalCenter
        }
    }

    Label {
        id: label

        anchors {
            top: parent.top
            //left: parent.left
            right: parent.right
            leftMargin: 16
        }
    }
}