import json
import sys
import argparse
from file import File
from meta import *

def generate_structure(dir: File):
    structure = []
    for f in dir:
        if f.isFile:
            structure.append({ 'name': f.name, 'length': f.length, 'hash': f.sha1, 'modified': f.modified })
        if f.isDirectory:
            structure.append({ 'name': f.name, 'children': generate_structure(f) })
    return structure

if __name__ == "__main__":
    if not indev:
        commit_sha = commit[:8] if len(commit) > 16 else commit
        commit_sha_in_short = commit_sha if len(commit) > 0 else 'dev'
        print(f'AppVersion: {version} ({commit_sha_in_short}), CompileTime: {compile_time}')

    # 解析参数
    parser = argparse.ArgumentParser(description='file comparer')
    parser.add_argument('source-dir', type=str, help='specify source directory to calculate structure data from')
    parser.add_argument('output-file', type=str, help='specify output file to save structure data')
    args = vars(parser.parse_args())

    arg_source_dir = args['source-dir']
    arg_output_file = args['output-file']

    source = File(arg_source_dir)
    output = File(arg_output_file)

    if not source.exists or source.isFile:
        print(f'directory not be found or not is a directory: {source.path}')
        sys.exit(1)
    
    print(f'calculating structure file for {arg_source_dir}. it will take some time')

    output.delete()
    output.content = json.dumps(generate_structure(source), ensure_ascii=False, indent=2)

    print(f'done')
