from _in_package import *
import config
import common
import runing_data


def traverse_dir(root_dir):
    print("正在遍历文件ing...")
    for path, dirs, files in os.walk(root_dir):
        path = common.formatting_path(path)
        for filename in files:
            runing_data.file_path_list.append(path + filename)
    print(f"完成\t总计 {len(runing_data.file_path_list)} 个文件")


def hash_files_from_glist(algorithm: function):
    print("正在计算文件散列ing...")
    i = 0
    p_old_i = -1
    for f_path in runing_data.file_path_list:
        with open(f_path, "rb") as f:
            f_hash = hashlib.file_digest(f, algorithm)
            runing_data.file_hash_results.append(runing_data.FileHashResult(f_path, f_hash.hexdigest(), algorithm.__name__))
            runing_data.hash_to_files[(f_hash.hexdigest(), algorithm.__name__)].append(f_path)
        i += 1
        if i % config.wait_c == 0:
            p_old_i = i
            print(f"\r{i}/{len(runing_data.file_path_list)}", end="")
    if p_old_i != -1 and i != p_old_i:
        print(f"\r{i}/{len(runing_data.file_path_list)}", end="")
    print()
    


def print_info(hash_to_files_list: list = runing_data.hash_to_files):
    size_total = 0
    size_if_one = 0
    print_size_total = 0
    print_size_if_one = 0
    for t in runing_data.hash_to_files:
        st_size = os.stat(runing_data.hash_to_files[t][0]).st_size
        size_total += st_size * len(runing_data.hash_to_files[t])
        size_if_one += st_size
        if st_size <= config.flag_size:
            continue
        print_size_total += st_size * len(runing_data.hash_to_files[t])
        print_size_if_one += st_size
        if len(runing_data.hash_to_files[t]) > 1:
            print(t, f"size: {st_size} Byte")
            for fp in runing_data.hash_to_files[t]:
                print("\t", fp)
    print()
    print(f"重复部分占用/总占用:\t{(size_total-size_if_one)//1024}KiB / {size_total//1024}KiB")
    print(f"占用大于 {config.flag_size} Byte 的文件中，重复部分占用/总占用:\t{(print_size_total-print_size_if_one)//1024}KiB / {print_size_total//1024}KiB")


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