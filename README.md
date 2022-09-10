# Back-up Tool

## The program for copying all data from source directory to destination folder, both specified as command line arguments. When file already exists in dst, the program calculate the hash (using sha256) of file and compare one to the src file hash. If the hashes don't match, src file will be copied and replaced with the dst file. Otherwise, the program will continue!  


```console
./back_up.py <src_dir> <dst_dir>
```