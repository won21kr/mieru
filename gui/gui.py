# -*- coding: utf-8 -*-
"""a GUI chooser"""

class GUI:
  def __init__(self, mieru):
    self.mieru = mieru

  def resize(self, w, h):
    """resize the GUI to given width and height"""
    pass

  def getWindow(self):
    """return the main window"""
    pass

  def getViewport(self):
    """return a (x,y,w,h) tuple"""
    pass

  def setWindowTitle(self, title):
    """set the window title to a given string"""
    pass

  def getToolkit(self):
    """report which toolkit the current GUI uses"""
    return

  def getAccel(self):
    """report if current GUI supports acceleration"""
    pass

  def toggleFullscreen(self):
    pass

  def startMainLoop(self):
    """start the main loop or its equivalent"""
    pass

  def stopMainLoop(self):
    """stop the main loop or its equivalent"""
    pass

  def showPreview(self, page, direction, onPressAction):
    """show a preview for a page"""
    pass

  def hidePreview(self):
    """hide any visible previews"""
    pass

  def getPage(self, flObject, name="", fitOnStart=True):
    """create a page from a file like object"""
    pass

  def showPage(self, page, mangaInstance=None, id=None):
    """show a page on the stage"""
    pass

  def getCurrentPage(self):
    """return the page that is currently shown
    if there is no page, return None"""
    pass

  def pageShownNotify(self, cb):
    """call the callback once a page is shown
    -> some large jpeg pages can take while to load"""
    pass

  def clearStage(self):
    pass

  def idleAdd(self, callback, *args):
    pass

  def statusReport(self):
    """report current status of the gui"""
    return "It works!"

  def newActiveManga(self, manga):
    """this is a new manga instance reporting that it has been loaded
    NOTE: this can be the first manga loaded at startup or a new manga instance
    replacing a previous one"""
    pass

  def getScale(self):
    """get current scale"""
    return None

  def getUpperLeftShift(self):
    return None

  def _destroyed(self):
    self.mieru.destroy()

  def _keyPressed(self, keyName):
    self.mieru.keyPressed(keyName)


def getGui(mieru, type="QML",accel=True, size=(800,480)):
  """return a GUI object"""
  if type=="hildon" and accel:
    import cluttergtk
    import clutter_gui
    return clutter_gui.ClutterGTKGUI(mieru, type, size)
  elif type=="QML" and accel:
    import qml_gui
    return qml_gui.QMLGUI(mieru, type, size)







