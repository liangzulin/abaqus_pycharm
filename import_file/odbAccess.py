from typing import Union
import os
import sys
"""
 =================================================
 | Copy from abaqus
 =================================================
"""
ON = 1
OFF = 0


class MaterialClass:
    def Elastic(self, table=None, type=None, temperatureDependency=OFF, dependencies=0, noCompression=OFF,
                noTension=OFF, moduli=None):
        pass


class Parts:
    def __init__(self):
        self.faces = Faces()

    def BaseShellExtrude(self, sketch, depth):
        pass

    def Set(self, faces, name):
        return Region()

    def SectionAssignment(self, region, sectionName, offset, offsetType, offsetField, thicknessAssignment):
        pass

    def seedPart(self, size, deviationFactor, minSizeFactor):
        pass

    def generateMesh(self):
        pass

    def setElementType(self, regions, elemTypes):
        pass

    def addNodes(self, nodeData, nodeSetName='nset-1'):
        pass

    def addElements(self, elementData, type, elementSetName=None, sectionCategory=None):
        # type: (object, str, str, SectionCategoryClass) -> None
        pass


class Faces:
    def getSequenceFromMask(self, mask):
        pass


class Region:
    def __init__(self):
        pass


"""
=====================================================
|    End of abaqus class
=====================================================
"""


def openOdb(path):
    # print(path)
    return Odb(path=path, name="", analysisTitle=None, description=None)


class Odb:

    def __init__(self, name, path, analysisTitle, description):
        self.not_run_yet = True
        self.rootAssembly = InstanceClass()
        assert isinstance(name, str)
        assert isinstance(path, str)
        self.name = name
        self.path = path
        self.analysisTitle = analysisTitle
        self.description = description

        self.abaqus_bat_path = 'abaqus'
        self.abaqus_bat_setting = 'noGUI'
        self.debug = True
        default_frame_list = [FrameClass()]
        self.steps = {'default_key': Step(default_frame_list)}

    def Part(self, name, embeddedSpace, type):
        return Parts()

    def Material(self, name):
        return MaterialClass()

    def HomogeneousShellSection(self, name, material, thickness):
        pass

    def SectionCategory(self, name, description):
        # type: (str, str) -> SectionCategoryClass
        return SectionCategoryClass()

    def Step(self, name, description, domain, timePeriod):
        # type: (str, str, str, float) -> StepClass
        return StepClass()

    def save(self, pathName=None):
        if self.not_run_yet:
            if isinstance(self.debug, bool) and self.debug:
                print(pathName)
            if 'ABAQUS_BAT_SETTING' in os.environ.keys():
                self.abaqus_bat_setting = os.environ['ABAQUS_BAT_SETTING']
            if 'ABAQUS_BAT_PATH' in os.environ.keys():
                self.abaqus_bat_path = os.environ['ABAQUS_BAT_PATH']
            self.not_run_yet = False
            os.system(self.abaqus_bat_path + ' cae -' + self.abaqus_bat_setting + ' ' + os.path.abspath(sys.argv[0]))

    def close(self):
        if self.not_run_yet:
            if 'ABAQUS_BAT_SETTING' in os.environ.keys():
                self.abaqus_bat_setting = os.environ['ABAQUS_BAT_SETTING']
            if 'ABAQUS_BAT_PATH' in os.environ.keys():
                self.abaqus_bat_path = os.environ['ABAQUS_BAT_PATH']
            self.not_run_yet = False
            os.system(self.abaqus_bat_path + ' cae -' + self.abaqus_bat_setting + ' ' + os.path.abspath(sys.argv[0]))


class Step:
    def __init__(self, frames):
        self.frames = frames


class SectionCategoryClass:
    def __init__(self):
        pass

    def SectionPoint(self, number, description):
        # type: (int, str) -> SectionPointClass
        return SectionPointClass()


class SectionPointClass:
    def __init__(self):
        pass


class StepClass:

    def __init__(self):
        pass

    def Frame(self, incrementNumber, frameValue, description):
        # type: (int, float, str) -> FrameClass
        return FrameClass()

    def setDefaultDeformedField(self, uField):
        # type: (FieldClass) -> None
        pass

    def setDefaultField(self, sField):
        # type: (FieldClass) -> None
        pass

    def HistoryRegion(self, name, description, point):
        # type: (str, str, SectionPointClass) -> HistoryRegionClass
        return HistoryRegionClass()


class HistoryRegionClass:
    def __init__(self):
        self.historyOutputs = {}
        self.subset = {}

    def HistoryOutput(self, name, description, type):
        his_obj = HistoryOutputClass()
        self.historyOutputs[name] = his_obj
        self.subset[name] = SubSetClass(self.historyOutputs)
        return his_obj

    def getSubset(self, variableName):
        return self.subset[variableName]


class SubSetClass:
    def __init__(self, historyOutputs=None, values=None):
        # type: (dict, list) -> None
        self.historyOutputs = historyOutputs
        self.values = values


class HistoryOutputClass:
    def __init__(self):
        self.data = None
        self.value = None

    def addData(self, frameValue=None, value=None, data=None):
        self.data = data
        self.value = value


class FrameClass:

    def __init__(self):
        self.fieldOutputs = {'RF': FieldOutputClass()}

    def FieldOutput(self, name, description, type, validInvariants=None):
        # type: (str, str, str, tuple) -> FieldClass
        return FieldClass()


class FieldOutputClass:
    def __init__(self):
        pass

    def getSubset(self, region):
        values = [RFOptClass('label1', [0, 0]),
                  RFOptClass('label2', [0, 0])]
        return SubSetClass(values=values)


class RFOptClass:
    def __init__(self, nodeLabel, data):
        self.nodeLabel = nodeLabel
        self.data = data


class FieldClass:

    def __init__(self):
        pass

    def addData(self, position, instance, labels, data, sectionPoint=None, localCoordSystem=None):
        # type: (str, InstanceElement, Union[tuple, list, range], Union[tuple, list], SectionPointClass, tuple) -> None
        if sectionPoint is not None:
            instance.nodes.append(sectionPoint)


class InstanceClass:

    def __init__(self):
        self.instances = {}
        self.nodeSets = {'All Node': '',
                         ' ALL NODES': ''}

    def Instance(self, name, object):
        # type: (str, str) -> InstanceElement
        ins_obj = InstanceElement(name, object)
        self.instances[name] = ins_obj
        return ins_obj




class InstanceElement:

    def __init__(self, name, object):
        """
        nodes list element should be SectionPointClass
        :param name:
        :param object:
        """
        self.nodes = []

    def ElementSetFromElementLabels(self, name, elementLabels):
        pass

    def assignSection(self, region, section):
        pass


def power(param, param1):
    # type: (HistoryOutputClass, float) -> HistoryOutputClass
    if param.data is not None:
        result_list = []
        for i in param.data:
            result_list.append(pow(i, param1))
        param.data = tuple(result_list)

    if param.value is not None:
        result_list = []
        for i in param.value:
            result_list.append(pow(i, param1))
        param.value = tuple(result_list)
    return param
