import sys
sys.path.append(r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries\_GitDoc")
import gitdoc

FILENAME = "PyDraw"
FOLDERPATH = r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries"
OUTPATH = r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries\PyDraw"
OUTNAME = "README"
EXCLUDETYPES = ["variable","module"]
gitdoc.DocumentModule(FOLDERPATH,
                  filename=FILENAME,
                  outputfolder=OUTPATH,
                  outputname=OUTNAME,
                  excludetypes=EXCLUDETYPES,
                  )
