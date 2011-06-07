"""
Mieru hildon UI (for Maemo 5@N900)
"""
import os
import gtk
import gobject
import hildon
import info

from base_platform import BasePlatform

class Maemo5(BasePlatform):
  def __init__(self, mieru):
    BasePlatform.__init__(self)

    self.mieru = mieru

    # enbale zoom/volume keys for usage by mieru
    self.enableZoomKeys(self.mieru.window)

    # add application menu
    menu = hildon.AppMenu()
    openFolderButton = gtk.Button("Open folder")
    openFolderButton.connect('clicked',self.startChooserCB, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
    openFileButton = gtk.Button("Open file")
    openFileButton.connect('clicked',self.startChooserCB, gtk.FILE_CHOOSER_ACTION_OPEN)
    fullscreenButton = gtk.Button("Fullscreen")
    fullscreenButton.connect('clicked',self.mieru.toggleFullscreen)

    # last open mangas list
    selector = hildon.TouchSelector()
    selector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
    self.historyStore = gtk.ListStore(gobject.TYPE_STRING)
    self.historyLocked = False
    self._updateHistory()
    selector.append_text_column(self.historyStore, False)
    selector.connect('changed', self._historyRowSelected)
    historyPickerButton = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,hildon.BUTTON_ARRANGEMENT_VERTICAL)
    historyPickerButton.set_title("History")
    historyPickerButton.set_selector(selector)
    self.mieru.watch('openMangasHistory', self._updateHistoryCB)

    optionsButton = gtk.Button("Options")
    optionsButton.connect('clicked',self._showOptionsCB)

    infoButton = gtk.Button("Info")
    infoButton.connect('clicked',self._showInfoCB)

    pagingButton = gtk.Button("Paging")
    pagingButton.connect('clicked',self.showPagingDialogCB)

    fittPickerButton = self._getFittingPickerButton("Page fitting")

    menu.append(openFileButton)
    menu.append(openFolderButton)
    menu.append(fullscreenButton)
    menu.append(historyPickerButton)
    menu.append(pagingButton)
    menu.append(fittPickerButton)
    menu.append(optionsButton)
    menu.append(infoButton)

    # Show all menu items
    menu.show_all()

    # Add the menu to the window
    self.mieru.window.set_app_menu(menu)

  def _getFittingSelector(self):
    """load fitting modes to the touch selector,
    also make active the last used fitting mode"""
    touchSelector = hildon.TouchSelector(text=True)
    touchSelector.set_column_selection_mode(hildon.TOUCH_SELECTOR_SELECTION_MODE_SINGLE)
    modes = self.mieru.getFittingModes()
    lastUsedValue = self.mieru.get('fitMode', None)
    lastUsedValueId = None
    id = 0
    for mode in modes:
      touchSelector.append_text(mode[1])
      if lastUsedValue == mode[0]:
        lastUsedValueId = id
      id+=1
    if lastUsedValue != None:
      touchSelector.set_active(0,lastUsedValueId)
    return touchSelector

  def _applyFittingModeCB(self, pickerButton):
    """handle the selector callback and set the appropriate fitting mode"""
    index = pickerButton.get_selector().get_active(0)
    modes = self.mieru.getFittingModes()
    try:
      (key, desc) = modes[index]
      self.mieru.set('fitMode',key)
    except Exception, e:
      print("maemo 5: wrong fitting touch selector index", e)

  def _getFittingPickerButton(self, title=None):
    """get a pciker button with an asociated touch selector,
    also load the last used value on startup"""
    fittPickerButton = hildon.PickerButton(gtk.HILDON_SIZE_AUTO,hildon.BUTTON_ARRANGEMENT_VERTICAL)
    if title:
      fittPickerButton.set_title(title)
    selector = self._getFittingSelector()
    fittPickerButton.set_selector(selector)
    fittPickerButton.connect('value-changed', self._applyFittingModeCB)
    return fittPickerButton


  def _showOptionsCB(self, button):
    self.showOptions()

  def showOptions(self):
    win = hildon.StackableWindow()
    win.set_title("Options")

    padding = 5
    vbox = gtk.VBox(False, padding)

    # page fitting
    pLabel = gtk.Label("Page")
    fittPickerButton = self._getFittingPickerButton("Page fitting")
    vbox.pack_start(pLabel, False, False, padding*2)
    vbox.pack_start(fittPickerButton, False, False, 0)

    # kinnetic scrolling
    ksLabel = gtk.Label("Scrolling")
    ksButton = self.CheckButton("Kinnetic scrolling")
    ksButton.set_active(self.mieru.get('kineticScrolling', False))
    ksButton.connect('toggled', self._toggleOptionCB, 'kineticScrolling', False)
    self.mieru.watch('kineticScrolling', self._updateKSCB, ksButton)
    vbox.pack_start(ksLabel, False, False, padding*2)
    vbox.pack_start(ksButton, False, False, 0)

    # clear history
    hLabel = gtk.Label("History")
    clearHistoryButton = self.Button("Clear history")
    clearHistoryButton.connect('clicked',self._clearHistoryCB)

    vbox.pack_start(hLabel, False, False, padding*2)
    vbox.pack_start(clearHistoryButton, False, False, 0)

    # debug
    debugLabel = gtk.Label("Debug")
    debug1Button = self.CheckButton("Print page loading info")
    debug1Button.set_active(self.mieru.get('debugPageLoading', False))
    debug1Button.connect('toggled', self._toggleOptionCB, 'debugPageLoading', False)
    vbox.pack_start(debugLabel, False, False, padding*2)
    vbox.pack_start(debug1Button, False, False, 0)

    # as options are too long, add a pannable area
    pann = hildon.PannableArea()
    pann.add_with_viewport(vbox)

    win.add(pann)

    win.show_all()

  def _toggleOptionCB(self, button, key, default):
    old = self.mieru.get(key, default)
    self.mieru.set(key, not old)

  def _updateKSCB(self, key, oldValue, newValue, button):
    button.set_active(newValue)


  def _showInfoCB(self, button):
    self.showInfo()

  def showInfo(self):
    win = hildon.StackableWindow()
    win.set_title("Info")

    """enlarge the tabs in the notebook vertically
    to be more finger friendly"""
    enlargeTabs = 15
    versionString = info.getVersionString()
    notebook = gtk.Notebook()
    
    # shortcuts need to be pannable
    pann = hildon.PannableArea()
    pann.add_with_viewport(info.getShortcutsContent())
    # add shortcuts tab
    notebook.append_page(pann,self._getLabel("Shortcuts",enlargeTabs))
    # add stats tab
    notebook.append_page(info.getStatsContent(self.mieru),self._getLabel("Stats", enlargeTabs))
    # add about tab
    notebook.append_page(info.getAboutContent(versionString),self._getLabel("About", enlargeTabs))

    # add the netebook to the new stackable window
    win.add(notebook)

    # show it
    win.show_all()

    # start on first page
    notebook.set_current_page(0)


  def _getLabel(self, name, spacing=0):
    """get a label fort notebook with adjustable spacing"""
    vbox = gtk.VBox(False, spacing)
    vbox.pack_start(gtk.Label(name),padding=spacing)
    vbox.show_all()
    return vbox




  def enable_zoom_cb(self, window):
    window.window.property_change(gtk.gdk.atom_intern("_HILDON_ZOOM_KEY_ATOM"), gtk.gdk.atom_intern("INTEGER"), 32, gtk.gdk.PROP_MODE_REPLACE, [1]);

  def disableZoomKeys(self):
    self.window.property_change(gtk.gdk.atom_intern("_HILDON_ZOOM_KEY_ATOM"), gtk.gdk.atom_intern("INTEGER"), 32, gtk.gdk.PROP_MODE_REPLACE, [0]);

  def enableZoomKeys(self,window):
          if window.flags() & gtk.REALIZED:
                  enable_zoom_cb(window)
          else:
                  window.connect("realize", self.enable_zoom_cb)

  def _updateHistoryCB(self, key=None, value=None, oldValue=None):
    print "update history"
    self._updateHistory()

  def _historyRowSelected(self, selector, column):
      if not self.historyLocked:
        try:
          id = selector.get_active(0)
          if id >= 0:
            state = self.currentHistory[id]['state']
            path = state['path']
            print "path selected: %s" % path
            activeMangaPath = self.mieru.getActiveMangaPath()
            if path != activeMangaPath: # infinite loop defence
              self.mieru.openMangaFromState(state)
        except Exception, e:
          print "error while restoring manga from history"
          print e
#      else:
#        print "history locked"


  def _updateHistory(self):
    """
    due to the fact that the touch selector emits the same signal when an
    item is selected like when an item is clicked on, we need to do this
    primitive locking
    """
    self.historyLocked = True
    sortedHistory = self.mieru.getSortedHistory()
    if sortedHistory:
      self.historyStore.clear()
      for item in sortedHistory:
        state = item['state']
        path = state['path']
        if state['pageNumber'] == None: # some states can have unknown last open page
          state['pageNumber'] = 0
        pageNumber = state['pageNumber']+1
        pageCount = state['pageCount']+1
        (folderPath,tail) = os.path.split(path)
        rowText = "%s %d/%d" % (tail, pageNumber, pageCount)

        self.historyStore.append((rowText,))
      self.currentHistory = sortedHistory
    self.historyLocked = False

  def _clearHistoryCB(self, button):
    self.mieru.clearHistory()
    self.historyLocked = True
    self.historyStore.clear()
    self.historyLocked = False


  def startChooserCB(self,button, type):
    self.startChooser(type)

  def startChooser(self, type):
    dialog = hildon.FileChooserDialog(self.mieru.window, type)
    lastFolder = self.mieru.get('lastChooserFolder', None)
    currentFolder = None
    selectedPath = None
    if lastFolder:
      dialog.set_current_folder(lastFolder)
    status = dialog.run()
    dialog.hide()
    if status == gtk.RESPONSE_OK:
      currentFolder = dialog.get_current_folder()
      selectedPath = dialog.get_filename()
    dialog.destroy()
    if currentFolder != None:
      self.mieru.set('lastChooserFolder', currentFolder)
    if selectedPath:
      self.mieru.openManga(selectedPath)

  def notify(self, message, icon=None):
    print message
#    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "", message)
    hildon.hildon_banner_show_information_with_markup(self.mieru.window, "icon_text", message)

  def pagingDialogBeforeOpen(self):
    """notify the user that the window in tha bakcground does not live-update"""
    self.notify("<b>Note:</b> the page in background does not refresh automatically", None)

  def minimize(self):
    """minimizing is not supported on Maemo :)"""
    self.notify('hiding to panel is not supported ona Maemo (no panel :)', None)

  def Button(self, label=""):
    """return hildon button"""
#    b = hildon.Button(gtk.HILDON_SIZE_AUTO_WIDTH | gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL)
    b = hildon.Button(gtk.HILDON_SIZE_FINGER_HEIGHT, hildon.BUTTON_ARRANGEMENT_VERTICAL)
    b.set_title(label)
    return b

  def CheckButton(self, label=""):
    """return hildon check button"""
    c = hildon.CheckButton(gtk.HILDON_SIZE_FINGER_HEIGHT)
    c.set_label(label)
    return c

