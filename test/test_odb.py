import json
from os import environ

try:
    from import_file.odbAccess import *
    from import_file.abaqusConstants import *
except ImportError as e:
    print(e, '\n\n\n\n\n\n')
    from odbAccess import *
    from abaqusConstants import *


environ['ABAQUS_BAT_PATH'] = 'D:\\SIMULIA\\Abaqus\\Commands\\abaqus'
environ['ABAQUS_BAT_SETTING'] = 'script'


class OpenOdb:
    def __init__(self):
        self.data_dir = 'D:\\data\\abqus_work_dir\\data\\rf_data'
        self.work_dir = 'D:\\data\\abqus_work_dir'

    def get_odb_paths(self):
        dr = self.work_dir
        ls = []
        for root, d, f in os.walk(top=dr, topdown=False):
            if root == dr:
                for file in f:
                    file_name, extension = os.path.splitext(file)
                    if extension == '.odb':
                        fp = dr + '/' + file
                        ls.append(fp)
        return ls

    @staticmethod
    def get_forces(odb_path):
        my_odb = openOdb(path=odb_path)
        all_steps = my_odb.steps
        step1 = list(all_steps.keys())[0]
        my_frame = all_steps[step1].frames[-1]  # type: FrameClass
        nodes_region = my_odb.rootAssembly.nodeSets[' ALL NODES']
        rf_opt = my_frame.fieldOutputs['RF'].getSubset(region=nodes_region).values  # type: list
        rf_data = map(lambda x: [x.nodeLabel, x.data[0], x.data[1]], rf_opt)
        rf_dict = {}
        for i in rf_data:
            rf_dict[i[0]] = {}
            rf_dict[i[0]]['fx'] = str(i[1])
            rf_dict[i[0]]['fy'] = str(i[2])

        node_dict = {}
        length = 0
        ins = my_odb.rootAssembly.instances
        for key in ins.keys():
            for node in ins[key].nodes:
                node_dict[node.label] = {}
                node_dict[node.label]['x'] = str(node.coordinates[0])
                node_dict[node.label]['y'] = str(node.coordinates[1])
                node_dict[node.label]['z'] = str(node.coordinates[2])
                if length < node.coordinates[1]:
                    length = node.coordinates[1]
        my_odb.close()
        return rf_dict, node_dict, length

    @staticmethod
    def calculate_data(rf_dict, node_dict, length):
        print(length)
        other_1 = {}
        rf = 0
        for i in rf_dict.keys():
            if node_dict[i] == -50:
                rf += rf_dict[i][0]
            else:
                other_1[i] = rf_dict[i]

    def get_data(self):
        odb_ls = self.get_odb_paths()
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        for p in odb_ls:
            f_dir, f_name = os.path.split(p)
            name, extension = os.path.splitext(f_name)
            if name[0] == 'E':
                rf_dict, node_dict, length = self.get_forces(p)
                with open(self.data_dir+'/rf_data-' + name + '.txt', 'w') as f:
                    f.write(json.dumps(rf_dict))
                    f.close()
                with open(self.data_dir+'/node_dict-' + name + '.txt', 'w') as f:
                    f.write(json.dumps(node_dict))
                    f.close()


if __name__ == '__main__':
    open_odb = OpenOdb()
    open_odb.get_data()
    path_list = open_odb.get_odb_paths()
    # path_list.append('abc_test')
    for path_single in path_list:
        open_odb.get_forces(path_single)
