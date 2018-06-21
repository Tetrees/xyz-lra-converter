
from distutils.core import setup
import py2exe

import glob
#import matplotlib
#from PIL import Image, PngImagePlugin
#import copy


# "PyQt4._qt",
         
includes = [
            "sip",
#            "copy",
#            "reportlab",
#            "reportlab.lib",
#            "reportlab.platypus",
#            "matplotlib.backends",
#            "matplotlib.backends.backend_qt4agg",
#            "matplotlib.figure",
#            "pylab",
            "numpy",
            "copy",
#            "scipy",
#            "scipy.sparse.csgraph._validation",                                 
#            "matplotlib.backends.backend_tkagg",
            ]
            
excludes = [
            '_gtkagg',
             '_tkagg',
             '_agg2', 
             '_cairo',
             '_cocoaagg',
             '_fltkagg',
             '_gtk',
             '_gtkcairo',
             ]
            
            
packages = [
            "PIL.Image",
            "PIL.PngImagePlugin",
            'reportlab',
#            'reportlab.graphics.charts',
#            'reportlab.graphics.samples',
#            'reportlab.graphics.widgets',
#            'reportlab.graphics.barcode',
#            'reportlab.graphics',
            'reportlab.lib',
            'reportlab.pdfbase',
            'reportlab.pdfgen',
            'reportlab.platypus',
]

dll_excludes = [
                'libgdk-win32-2.0-0.dll',
                'libgobject-2.0-0.dll'
                ]

opts = {
      'py2exe': { "includes" : includes,
                   'excludes': excludes,
                   'dll_excludes': dll_excludes,
                   "packages": packages
                 }
         }
data_f = [('images', [r'C:\temp\add.png',
#                      r'C:\temp\app_icon1.png',
                      r'C:\temp\remove.png',
                      r'C:\temp\export.png',
                      r'C:\temp\import.png',
                      r'C:\temp\report.png'
                      ])]
#[(r'mpl-data', glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\*.*')),
#                   (r'mpl-data', [r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
#                    (r'mpl-data\images',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
#                    (r'mpl-data\fonts',glob.glob(r'C:\Python25\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))
#         ]


setup(
        windows=[{"script" : "XYZLRAconverter.py"}],
        options = opts,
        data_files = data_f
        )

