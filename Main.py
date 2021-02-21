import file_parser as fp
import VM_parser as vmp
import sys
import os.path

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('No folder was specified. please enter a file or folder'
              'name in system args.')
    else:
        for i in range(1, len(sys.argv)):
            file_list = fp.directory_parser(sys.argv[i])
            dir_name = fp.get_dir_name(sys.argv[i])
            accumulated_code = []
            for path in file_list:
                try:
                    lines = fp.file_reader(path)
                    name = fp.name_extractor(path)
                    accumulated_code += vmp.init()
                    accumulated_code += vmp.translate(lines, name)
                except SyntaxError as e:
                    print("Error translating file:\n{0}"
                          "\nwith Error:\n{1}".format(path, e.msg))
                except IOError as e:
                    print("Error parsing file:\n{0}\nwith Error:\n{1}".format(path, e.strerror))
            vm_path = file_list[0]
            if os.path.isdir(sys.argv[i]):
                dir_name += '.vm'
                dir_path = os.path.abspath(sys.argv[i])
                vm_path = os.path.sep.join([dir_path, dir_name])
            fp.file_writer(accumulated_code, vm_path)

