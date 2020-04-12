import itertools
import signal
import subprocess
import sys

separator = '==============================================\n'
usage = '''
Usage:
namebuster <names|url|file>\n
Example (names): namebuster "John Broccoli, Diana Mango"
Example (url):   namebuster https://sauna.htb
Example (file):  namebuster document.txt
'''
banner = '''
  _   _    _    __  __ _____ ____  _   _    ____      _____     _____ ____
 | \ | |  / \  |  \/  | ____| __ )| | | |  / ___|   _|_   _|   | ____|  _ \\
 |  \| | / _ \ | |\/| |  _| |  _ \| | | |  \___ \ _| |_| |_____|  _| | |_) |
 | |\  |/ ___ \| |  | | |___| |_) | |_| |   ___) |_   _| |_____| |___|  _ <
 |_| \_/_/   \_\_|  |_|_____|____(_)___/___|____/  |_| |_|     |_____|_| \_\\
                                      |_____|
'''


def signal_handler(sig, frame):
    print('\nExiting...\n' + separator)
    sys.exit(0)


def name_with_symbol(name_list):
    results = []

    for name in name_list:
        results.append(name + '.')
        results.append(name + '_')
        results.append(name + '-')
        results.append(name + '+')

    return results


def combine(left, right):
    left.extend(name_with_symbol(left))
    return map(''.join, itertools.product(left, right))


def generate(names, cli=False, name_sep=False):
    results = {}
    total_variations = []

    for name in names:
        name_variations = []

        split_name = name.split(' ')
        # TODO: Improve this
        if len(split_name) != 2:
            print('Invalid name provided, must match "FirstName LastName" format')
            continue

        first_name = split_name[0]
        last_name = split_name[1]

        first_name_vars = [first_name.lower(), first_name.capitalize(), first_name.upper()]
        last_name_vars = [last_name.lower(), last_name.capitalize(), last_name.upper()]

        name_variations.extend(combine(first_name_vars[:] + [first_name[0].lower(), first_name[0].upper()], last_name_vars[:]))
        name_variations.extend(combine(last_name_vars[:] + [last_name[0].lower(), last_name[0].upper()], first_name_vars[:]))
        name_variations.extend(combine(first_name_vars[:], [last_name[0].lower(), last_name[0].upper()]))
        name_variations.extend(combine(last_name_vars[:], [first_name[0].lower(), first_name[0].upper()]))

        name_variations.extend(first_name_vars)
        name_variations.extend(last_name_vars)

        results[name] = name_variations
        total_variations.extend(name_variations)

    # Show prompt for what to do with the names if not being piped to file
    if sys.stdout.isatty():
        cli_prompt(results, total_variations)
    elif cli:
        for variation in total_variations:
            print(variation)
    else:
        if name_sep:
            return results
        else:
            return total_variations


def cli_prompt(results, variations):
    print(str(len(results)) + ' user(s), ' + str(len(variations)) + ' variations\n')
    print('Pick a user to view their username permutations, or write to a file:\n')
    prompt = ''
    i = 0
    for name in results.keys():
        prompt += str(i) + ') ' + name + '\n'
        i += 1

    prompt += str(i) + ') Write to file\n'
    print(prompt)
    action = int(input('Choice (0-' + str(i) + '): '))
    if action >= len(results):
        filename = input('File name: ')
        with(open(filename, 'w')) as users_file:
            for variation in variations:
                users_file.write(variation + '\n')
    else:
        for variation in results[list(results.keys())[action]]:
            print(variation)
        print(separator)
        cli_prompt(results, variations)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    if len(sys.argv) <= 1:
        print(usage)
        sys.exit(1)

    # TODO: Add separate args for parsing name list vs file vs url
    print(banner)
    names = [name.strip() for name in sys.argv[1].split(',')]
    generate(names, cli=True)
