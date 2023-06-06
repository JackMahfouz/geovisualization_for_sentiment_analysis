import os
import sys
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
from Modules.utils import sentiment_clossifier, df_to_shp
# from PyQt5 import QtGui
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'gui.ui'))
class Sentiment_Classifier(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Sentiment_Classifier, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.pbgo.clicked.connect(self.doStuff)
    def goPrint(self):
        print("hi jack......")
    def doStuff(self):
        x, y, aspect, text = self.xvalue.text(), self.yvalue.text(), self.aspects.text(), self.text.text()
        inpath = self.infile.text()
        outpath = self.outdir.text()
        filename = self.filenamestr.text()
        if outpath[-1] != '/' or outpath[-1] != '\\':
            if '/' in outpath:
                outpath =outpath+'/'
            elif '\\' in outpath:
                outpath =outpath+'\\'
            else: outpath =outpath+'/'
        data = sentiment_clossifier(inpath, aspect, text, x, y)
        data.to_csv(outpath+filename)
        QtGui.QMessageBox.question(self, "done")
def run():
    app = QtWidgets.QApplication(sys.argv)
    window = Sentiment_Classifier()
    window.show()
    sys.exit(app.exec_())
    
run()
