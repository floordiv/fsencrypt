import os
import sys
import hashlib


config = {
    'ignore': ['fsencrypt.py'],
    'walkdir': False,
    'path': '.'
}


def crypt_file(_file):
    if _file not in config['ignore']:
        with open(_file) as source_file:
            source = source_file.read()

        try:
            with open(_file + '.sha256', 'w') as encrypted_file:
                encrypted_file.write(hashlib.sha256(source.encode()).hexdigest())

            print('Encrypted: "{}"'.format(_file))
        except Exception as exc:
            print('Failed to encrypt "{}":'.format(_file), exc)


def main():
    if bool(config['walkdir']):
        files_to_encrypt = []
        for _dir, _, files in list(os.walk(config['path'])):
            files_to_encrypt += [_dir + '/' + _file for _file in files]

    else:
        files_to_encrypt = os.listdir(config['path'])

    for _file in files_to_encrypt:
        crypt_file(_file)


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) > 1 and not args[0].startswith('--'):
        config['path'] = args[0]  # constant. Path is the first argument or current folder

    for arg, val in [('--recursive', 'walkdir')]:
        try:
            if arg in args:
                config[val] = args[args.index(arg) + 1]
        except IndexError:
            print('[ERROR] Missing value for argument:', arg)

    result = []

    for file in config['ignore']:
        if ',' in file:
            result += file.split(',')
        else:
            result += file

    config['ignore'] = result

    main()
