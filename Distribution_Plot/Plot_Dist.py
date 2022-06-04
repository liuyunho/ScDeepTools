import Sccater_Interactive
from CodeScript.utils import Single_Cell_Data
import pandas as pd
import sys
from matplotlib.backends.qt_compat import QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class ColumnNamesError(Exception):  # 继承异常类
    def __init__(self, Description):
        print(Description)

def Plot_Dist(CoordinateData, AnnotationData):
    data = pd.read_csv(CoordinateData)
    anno = pd.read_csv(AnnotationData)
    if sum(data.columns==['CellBarcode', 'Coor1', 'Coor2', 'CellLabel']) < 4:
        raise ColumnNamesError('The column name of Coordinate Data must be:'
                               'CellBarcode, Coor1, Coor2, CellLabel')
    if sum(anno.columns==['CellLabel', 'Annotation', 'Color']) < 3:
        raise ColumnNamesError('The column name of Annotation Data must be:'
                               'CellLabel, Annotation, Color')
    color_dict = dict(zip(anno['CellLabel'],anno['Color']))
    label_dict = dict(zip(anno['CellLabel'],anno['Annotation']))
    singledata = Single_Cell_Data(data['CellBarcode'], data['Coor1'], data['Coor2'],
                                                      data['CellLabel'], color_dict, label_dict)
    FigureCanvas = FigureCanvasQTAgg
    # Must come before any Qt widgets are made
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(1, 1, 1)
    dis_coll = Sccater_Interactive.Distribution_Display(ax, singledata.group, singledata.color_dict)
    ax.autoscale(True)
    ctrl_sys = Sccater_Interactive.ControlSys(fig, ax, singledata, dis_coll.collection, singledata.color_dict)
    win.resize(int(fig.bbox.width), int(fig.bbox.height))
    win.setWindowTitle("Embedding with Qt")
    # Needed for keyboard events
    canvas.setFocusPolicy(QtCore.Qt.StrongFocus)
    canvas.setFocus()
    win.setCentralWidget(canvas)
    win.show()
    sys.exit(app.exec_())

#if __name__=='__main__':
#    Plot_Dist("/3data/cuidanni/pycharm/Data/CoordinateData.csv"
#              , "/3data/cuidanni/pycharm/Data/AnnotationData.csv")