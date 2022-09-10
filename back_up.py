import sys
import os
import shutil
import time

import hashlib

from pyfiglet import Figlet

src_file_counter = 0
src_dir_counter = 0
dst_file_counter = 0
dst_dir_counter = 0


def cmp_file_hash(src: str, dst: str) -> bool:
    """
    Compare hashes of two files
    :param src:
    :param dst:
    :return:
    """
    src_hash = hashlib.new('sha256')
    dst_hash = hashlib.new('sha256')

    with open(src, 'rb') as f:
        src_content = f.read()
    with open(dst, 'rb') as f:
        dst_content = f.read()

    src_hash.update(src_content)
    dst_hash.update(dst_content)

    return src_hash.digest() == dst_hash.digest()


def travel_dir(src_dir, dst_dir):
    global src_file_counter, src_dir_counter, \
        dst_file_counter, dst_dir_counter

    for item in os.listdir(src_dir):
        full_path_src, full_path_dst = os.path.join(src_dir, item), os.path.join(dst_dir, item)  # make full path

        if os.path.isdir(full_path_src):
            src_dir_counter += 1
            if not os.path.exists(full_path_dst):
                os.makedirs(full_path_dst)
                dst_dir_counter += 1

            travel_dir(full_path_src, full_path_dst)

        elif os.path.isfile(full_path_src):
            src_file_counter += 1
            if not os.path.exists(full_path_dst) or not cmp_file_hash(full_path_src, full_path_dst):
                shutil.copy(full_path_src, full_path_dst)
                dst_file_counter += 1


def main():
    global src_file_counter, src_dir_counter, \
        dst_file_counter, dst_dir_counter

    preview_text = Figlet(font='slant')
    print(preview_text.renderText('BACK-UP'), '\n')

    if len(sys.argv) < 3:
        print(f'[-] Usage: python {sys.argv[0]} <source_file> <target_file>\n')
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print('[-] Source file does not exist!\n')
        sys.exit(1)

    print(f'[+] Copying data of {sys.argv[1]} to {sys.argv[2]}\n')

    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])

    start = time.time()

    try:
        """
        Handle exception if stack overflow because of too many function calls 
        
        """
        travel_dir(sys.argv[1], sys.argv[2])

    except RecursionError:
        print('[-] Too many files!')
        sys.exit(1)
    finally:
        """
        Program  work report
        """
        end = time.time()

        print(f'\t\t\t\tSummary\n')
        print(f'[!] Start: {s_time(start)}\tFinish: {s_time(end)}\tTook time: {round(end - start, 2)} sec\n')

        print(f'[!] In src: {src_dir_counter} dirs {src_file_counter} files, '
              f'Copy to dst: {dst_dir_counter} dirs {dst_file_counter} files\n')


def s_time(my_time):
    return time.strftime("%H:%M:%S", time.localtime(my_time))


if __name__ == '__main__':
    main()

    input("Press any key...\n")
