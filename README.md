# abaqus_pycharm
allow pycharm IDE check types and run abaqus python program

  1. copy the files from import_file folder to python interpreter's site-package.
  2. set the pycharm's interpreter to step 1's interpreter.
  3. add the follow environment variable into your abaqus python code.
 
```python
from os import environ
environ['ABAQUS_BAT_PATH'] = 'D:\\SIMULIA\\Abaqus\\Commands\\abaqus'
environ['ABAQUS_BAT_SETTING'] = 'noGUI'
```

Detail mechanics:

This project rewrite the mdb's saveAs method:

```python
mdb.saveAs(pathName='some_name')
``` 

The detail code in the saveAs function is:

```python
def saveAs(self, pathName):
    if isinstance(self.debug, bool) and self.debug:
        print(pathName)
    if 'ABAQUS_BAT_SETTING' in os.environ.keys():
        self.abaqus_bat_setting = os.environ['ABAQUS_BAT_SETTING']
    if 'ABAQUS_BAT_PATH' in os.environ.keys():
        self.abaqus_bat_path = os.environ['ABAQUS_BAT_PATH']
    os.system(self.abaqus_bat_path + ' cae -' + self.abaqus_bat_setting + ' ' + os.path.abspath(sys.argv[0]))
```
