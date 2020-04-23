import os
import sys
import hashlib


config = {
    'ignore': ['./fsencrypt.py', './README.md', './.git'],
    'walkdir': False,
    'path': '.',
    'remove-source': False
}


def crypt_file(_file):
    if _file not in config['ignore']:
        try:
            with open(_file) as source_file:
                source = source_file.read()
        except UnicodeDecodeError:
            print('Failed to encrypt "{}": unable to decode'.format(_file))

        if config['remove-source']:
            os.remove(_file)

        try:
            with open(_file + '.sha256', 'w') as encrypted_file:
                encrypted_file.write(hashlib.sha256(source.encode()).hexdigest())

            print('Encrypted: "{}"'.format(_file))
        except Exception as exc:
            print('Failed to encrypt "{}":'.format(_file), exc)


def main():
    config['remove-source'] = bool(config['remove-source'])

    if bool(config['walkdir']):
        files_to_encrypt = []
        for _dir, _, files in list(os.walk(config['path'])):
            if _dir not in config['ignore'] and True not in [_dir.startswith(i) for i in config['ignore']]:
                files_to_encrypt += [_dir + '/' + _file for _file in files]

    else:
        files_to_encrypt = os.listdir(config['path'])

    for _file in files_to_encrypt:
        crypt_file(_file)


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) > 1 and not args[0].startswith('--'):
        config['path'] = args[0]  # constant. Path is the first argument or current folder

    for arg, val in [('--recursive', 'walkdir'),
                     ('--rewrite', 'remove-source'),
                     ('--ignore', 'ignore')]:
        try:
            if arg in args:
                if isinstance(config[val], list):   # just append values
                    config[val].append(args[args.index(arg) + 1])
                else:
                    config[val] = args[args.index(arg) + 1]
        except IndexError:
            print('[ERROR] Missing value for argument:', arg)

    result = []

    for file in config['ignore']:
        if ',' in file:
            result += file.split(',')
        else:
            result += [file]

    config['ignore'] = result

    main()
