//MainView.qml
//import Qt 4.7
import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

Page {
    id : mainView
    anchors.fill : parent
    tools : mainViewToolBar

    property int maxPageNumber : 2
    property int pageNumber : 1
    property string mangaPath : ""
    property string lastUrl
    property bool rememberScale : options.get("QMLRememberScale", false)

    onMangaPathChanged : { reloadPage() }
    onPageNumberChanged : { reloadPage() }

    // workaround for calling python properties causing segfaults
    function shutdown() {
        //console.log("main view shutting down")
    }

    function reloadPage() {
        //console.log("** reloading page **")
        var pageIndex = pageNumber-1
        var url = "image://page/" + mangaPath + "|" + pageIndex;
        // check for false alarms
        if (url != lastUrl) {
          //console.log(mangaPath + " " + pageNumber)
          mangaPage.source = url
          // reset the page position
          pageFlickable.contentX = 0;
          pageFlickable.contentY = 0;
          //update page number in the current manga instance
          //NOTE: this is especialy important due to the slider
          readingState.setPageID(pageIndex, mangaPath);
        }
     }

    function showPage(path, pageId) {
        mainView.mangaPath = path
        var pageNr = pageId+1
        mainView.pageNumber = pageNr
    }

    // ** trigger notifications
    function notify(text) {
        notification.text = text;
        notification.show();
    }

    // ** fullscreen handling
    function toggleFullscreen() {
        console.log("toggle toolbar");
        /* handle fullscreen button hiding
        it should be only visible with no toolbar */
        fullscreenButton.visible = !fullscreenButton.visible
        rootWindow.showToolBar = !rootWindow.showToolBar;
    }

    ToolBarLayout {
        id : mainViewToolBar
        visible: false
        ToolIcon { iconId: "toolbar-view-menu"; onClicked: mainViewMenu.open() }
        //ToolIcon { iconId: "toolbar-previous" }
        ToolButton { id : pageNumbers
                     //text : 0/1
                     text : mainView.pageNumber + "/" + mainView.maxPageNumber
                     height : parent.height
                     flat : true
                     onClicked : { pagingDialog.open() }
        }
        //ToolIcon { iconId: "toolbar-next" }
        ToolIcon { iconId: "toolbar-down"
                   onClicked: mainView.toggleFullscreen() }
        //ToolIcon { iconSource: "image://icons/view-normal.png"; onClicked: mainView.toggleFullscreen() }
        }

    Menu {
        id : mainViewMenu

        MenuLayout {
            MenuItem {
              text : "Open file"
              onClicked : {
                  fileSelector.down(readingState.getSavedFileSelectorPath());
                  fileSelector.open();
            }
        }

            MenuItem {
                text : "History"
                onClicked : {
                    rootWindow.openFile("HistoryPage.qml")
                    }
            }

            MenuItem {
                text : "Options"
                onClicked : {
                    rootWindow.openFile("OptionsPage.qml")
                    }
            }

            MenuItem {
                text : "Info"
                onClicked : {
                    rootWindow.openFile("InfoPage.qml")
                }
            }
        }
    }

    PinchArea {
        //anchors.fill : parent
        //onPinchStarted : console.log("pinch started")
        //pinch.target : mangaPage
        //pinch.minimumScale: 0.5
        //pinch.maximumScale: 2
        width: Math.max(pageFlickable.contentWidth, pageFlickable.width)
        height: Math.max(pageFlickable.contentHeight, pageFlickable.height)
        property real initialScale
        property real initialWidth
        property real initialHeight

        onPinchStarted: {
            initialScale = pageFlickable.scale
            initialWidth = pageFlickable.contentWidth
            initialHeight = pageFlickable.contentHeight
            //pageFlickable.interactive = false
            //console.log("start " + pinch.scale)
        }

        onPinchUpdated: {
            // adjust content pos due to drag
            pageFlickable.contentX += pinch.previousCenter.x - pinch.center.x
            pageFlickable.contentY += pinch.previousCenter.y - pinch.center.y

            // resize content
            pageFlickable.resizeContent(initialWidth * pinch.scale, initialHeight * pinch.scale, pinch.center)
            // remember current scale
            pageFlickable.scale = initialScale * pinch.scale

            //console.log("pf " + pageFlickable.contentWidth + " " + pageFlickable.contentHeight)
            //console.log("page " + mangaPage.width + " " + mangaPage.height)
            //console.log("scale " + pageFlickable.scale)

        }

        onPinchFinished: {
            //pageFlickable.interactive = true
            // Move its content within bounds.
            pageFlickable.returnToBounds()
            if (mainView.rememberScale) {
                options.set("QMLMangaPageScale", pageFlickable.scale)
            }
        }
    }

    MouseArea {
        anchors.fill : parent
        id: prevButton
        objectName: "prevButton"
        drag.filterChildren: true
        onClicked: {
            if (mouseX < width/2.0){
                console.log("previous page");
                readingState.previous();
            }

            else{
                console.log("next page");
                readingState.next();
            }
        }

        Flickable {
            id: pageFlickable
            property real scale: mainView.rememberScale ? options.get("QMLMangaPageScale", 1.0) : 1.0
            objectName: "pageFlickable"
            anchors.fill : parent
            contentWidth : mangaPage.width
            contentHeight : mangaPage.height

            Image {
                id: mangaPage
                width : sourceSize.width * pageFlickable.scale
                height : sourceSize.height * pageFlickable.scale
                //smooth : !pageFlickable.moving
                smooth : true
                //width : pageFlickable.contentWidth
                //height : pageFlickable.contentHeight
                // update flickable width once an image is loaded
                onSourceChanged : {
                    //console.log("SOURCE")
                    //console.log(sourceSize.width + " " + sourceSize.height)
                    //console.log(width + " " + height)


                    // reset or remeber scale
                    if (!mainView.rememberScale) {
                        pageFlickable.scale = 1.0
                    }
                    //pageFlickable.contentWidth = sourceSize.width * pageFlickable.scale
                    //pageFlickable.contentHeight = sourceSize.height * pageFlickable.scale
                }
            }
        }
    }

    ToolIcon {
        id : fullscreenButton
        //source : "image://icons/view-fullscreen.png"
        iconId: "toolbar-up"
        anchors.right : mainView.right
        anchors.bottom : mainView.bottom
        visible : false
        opacity : 0.1
        width : Math.min(parent.width,parent.height)/8.0
        height : Math.min(parent.width,parent.height)/8.0
        MouseArea {
            anchors.fill : parent
            drag.filterChildren: true
            onClicked: mainView.toggleFullscreen();
        }
    }

    Menu {
        id : pagingDialog
        MenuLayout {
            //width : pagingDialog.width
            id : mLayout
            Row {
                //anchors.left : mLayout.left
                //anchors.right : mLayout.right
                Slider {
                    id : pagingSlider
                    width : mLayout.width*0.9
                    //anchors.topMargin : height*0.5
                    //anchors.left : mLayout.left
                    maximumValue: mainView.maxPageNumber
                    minimumValue: 1
                    value: mainView.pageNumber
                    stepSize: 1
                    valueIndicatorVisible: false
                    //orientation : Qt.Vertical
                    onPressedChanged : {
                        //only load the page once the user stopped dragging to save resources
                        mainView.pageNumber = value
                    }

            }

                CountBubble {
                    //width : mLayout.width*0.2
                    //anchors.left : pagingSlider.righ
                    //anchors.right : mLayout.right
                    value : pagingSlider.value
                    largeSized : true
                }
            }
        }
    }
}