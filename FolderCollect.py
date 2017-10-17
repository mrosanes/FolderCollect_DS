import os

from PyTango import AttrWriteType, DevState
from PyTango.server import Device, DeviceMeta, attribute, run


class FolderCollect(Device):
    __metaclass__ = DeviceMeta

    FolderNum = attribute(label="FolderNum", dtype=float,
                          access=AttrWriteType.READ_WRITE,
                          fget="get_FolderNum", fset="set_FolderNum",
                          doc="the folder number")

    RootFolder = attribute(label="RootFolder", dtype=str,
                           access=AttrWriteType.READ_WRITE,
                           fget="get_RootFolder", fset="set_RootFolder",
                           doc="the root folder to store the collected data")

    def init_device(self):
        Device.init_device(self)
        self.set_state(DevState.ON)
        # to be changed by: /beamlines/bl09/projects/rawdata
        self._root_folder = "/beamlines/bl09/controls/DEFAULT_USER_FOLDER/"
        self._folder_num = 0
        self._user_folder = self._root_folder + "data_" + str(self._folder_num)
        os.system("mkdir -p %s" % self._user_folder)

        # This is the link name (not a folder): 
        # It is the place that has to be indicated in the XMController SW
        # to store the data:
        self._all_files_link = "/beamlines/bl09/controls/BL09_RAWDATA"

        # The data will be distributed in different folders thanks to setting
        # the folder number. All data stored in the symbolic link, 
        # will be stored in the user folder.
        os.system("ln -s %s %s" % (self._user_folder, self._all_files_link))

    def get_RootFolder(self):
        return self._root_folder
        
    def set_RootFolder(self, root_folder):
        self._root_folder = root_folder
        print("Root Folder set to %s" % self._root_folder)

    def get_FolderNum(self):
        return self._folder_num
        
    def set_FolderNum(self, folder_num):
        self._folder_num = folder_num
        self._user_folder = self._root_folder + "/data_" + str(int(folder_num))
        os.system("rm %s" % self._all_files_link)
        os.system("mkdir -p %s" % self._user_folder)
        os.system("ln -s %s %s" % (self._user_folder, self._all_files_link))
        print("Folder set to %s" % self._user_folder)

    def delete_device(self):
        os.system("rm %s" % self._all_files_link)


if __name__ == "__main__":
    run([FolderCollect])