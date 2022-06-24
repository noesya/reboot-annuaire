import json
import os
import re
import unicodedata
import yaml


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
    del line[:9]
    del line[-1]

# get first line
header = list.pop(0)
domainsList = []

for column in list:
    file = slugify(column[0] + "-" + column[1])
    if not os.path.exists('content/partners/' + file + '.md'):
        if column[4] == "X":
            domainsList.append("developpement-durable")
        if column[5] == "X":
            domainsList.append("rse-rso")
        if column[6] == "X":
            domainsList.append("numerique")
        if column[7] == "X":
            domainsList.append("marketing")
        if column[8] == "X":
            domainsList.append("communication")
        if column[9] == "X":
            domainsList.append("medias-et-influence")
        if column[10] == "X":
            domainsList.append("design-et-ecoconception")
        if column[14] == "Sélectionnez une région":
            column[14] = ""

        data = f'{{"title" : "{column[0]} {column[1]}", "description": "{column[2]}", "career": "{column[3]}", "domains": {json.dumps(domainsList)}, "services": "{column[11]}", "phone": "{column[12]}", "email": "{column[13]}", "regions": "{slugify(column[14])}", "remote": "{column[15]}", "linkedin": "{column[16]}", "website": "{column[17]}", "conditions": "{column[18]}"}}'
        data = json.loads(data)
        domainsList = []

        # create new file with content
        open('content/partners/' + file + '.md', 'x').write(
            yaml.dump(data, explicit_start=True, allow_unicode=True) + "---")
