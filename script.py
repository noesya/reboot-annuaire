import json
import os
import re
import unicodedata


# slugify script
def slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def _slugify(value, allow_unicode=False):
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '_', value).strip('-_')

list = []
line_number = 0
with open('inscription_dans_lannuaire_reboot_dune_personne_intervenante_dans_les_ecoles___reboot_2022.tsv',
          'r') as input_file:
    for line in input_file:
        if line_number > 1:
            # delete double quotes
            line = line.replace('\"', '')
            # parse .tsv in list
            list.append(line.split('\t'))
        else:
            line_number += 1

for line in list:
    # delete useless columns and characters
    del line[1:9]
    del line[-1]

# get first line
header = list.pop(0)

for column in list:
    file = slugify(column[1] + "-" + column[2])
    if not os.path.exists('content/partners/' + file + '.md'):
        # convert list to .json
        json_dict = {}
        for i in range(len(header)):
            json_dict[_slugify(header[i])] = column[i]

        # create new file with content
        open('content/partners/' + file + '.md', 'x').write(json.dumps(json_dict, ensure_ascii=False))
