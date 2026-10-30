from _in_package import *
import config
import common
import runing_data


def traverse_dir(root_dir):
    for path, dirs, files in os.walk(root_dir):
        path = common.formatting_path(path)
        for filename in files:
            runing_data.file_path_list.append(path + filename)


def hash_files_from_glist(algorithm: function):
    for f_path in runing_data.file_path_list:
        with open(f_path, "rb") as f:
            f_hash = hashlib.file_digest(f, algorithm)
            runing_data.file_hash_results.append(runing_data.FileHashResult(f_path, f_hash.hexdigest(), algorithm.__name__))
            runing_data.hash_to_files[(f_hash.hexdigest(), algorithm.__name__)].append(f_path)


def print_info():
    for t in runing_data.hash_to_files:
        if len(runing_data.hash_to_files[t]) > 1:
            st_size = os.stat(runing_data.hash_to_files[t][0]).st_size
            if st_size <= config.flag_size:
                continue
            print(t, f"size: {st_size} Byte")
            for fp in runing_data.hash_to_files[t]:
                print("\t", fp)
            print()


def reg_opts():
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--path", default=None, required=False)
    parser.add_argument("--fsize", default=None, required=False, help="只打印文件大小大于fsize Byte的重复文件")
    args = parser.parse_args()
    if args.path != None:
        config.work_dir = args.path
    if args.fsize != None:
        config.flag_size = int(args.fsize)

reg_opts()

if not os.path.exists(config.work_dir):
    exit(-1)

traverse_dir(config.work_dir)
hash_files_from_glist(hashlib.sha256)

print_info()