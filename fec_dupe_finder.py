
import pandas as pd
from fuzzywuzzy import fuzz
import csv
import numpy as np
import string

nicknames = {'abbie': ['abigail'], 'abby': ['abigail'], 'abe': ['abraham'], 'abram': ['abraham'], 'al': ['allan', 'alan', 'allen'], 'alec': ['alexander'], 
'alex': ['alexander'], 'allie': ['alison', 'allison'], 'ally': ['alison', 'allison'], 'andy': ['andrew'], 'ann': ['annette', 'anna', 'anne'], 
'annie': ['ann', 'anna', 'anne', 'annette'], 'archie': ['archibald'], 'bart': ['bartholomew'], 'bea': ['beatrice'], 'becky': ['rebecca', 'rebekah'], 
'becca': ['rebecca', 'rebekah'], 'bella': ['isabel', 'isabella'], 'belle': ['isabel', 'isabella'], 'ben': ['benjamin', 'benadict'], 'benny': ['benjamin'], 
'bert': ['bertram', 'robert', 'albert'], 'bertie': ['bertha', 'roberta'], 'berty': ['bertha', 'roberta'], 'bess': ['elizabeth', 'elisabeth'], 
'bessie': ['elizabeth', 'elisabeth'], 'bessy': ['elizabeth', 'elisabeth'], 'beth': ['elizabeth', 'elisabeth'], 'betsy': ['elizabeth', 'elisabeth'], 
'betty': ['elizabeth', 'elisabeth'], 'bex': ['rebecca', 'rebekah'], 'bill': ['william'], 'billy': ['william'], 'bob': ['robert'], 'bobby': ['robert'], 
'bobbie': ['roberta'], 'carrie': ['caroline', 'carol'], 'cate': ['caitlin', 'caitlyn', 'catherine'], 'cathie': ['catherine'], 'cathy': ['catherine'], 
'charlie': ['charles'], 'chris': ['christopher', 'christina'], 'chrissie': ['christina'], 'christie': ['christina'], 'chuck': ['charles'], 
'cindy': ['lucinda', 'cynthia'], 'claire': ['clara', 'clarice', 'clarissa'], 'claud': ['claudius'], 'connie': ['constance', 'cornelia'], 'dan': ['daniel'], 
'dani': ['danielle', 'daniella'], 'danny': ['daniel'], 'dave': ['david'], 'deb': ['debrah', 'debra', 'deborah'], 'debbie': ['debrah', 'debra', 'deborah'], 
'debby': ['debrah', 'debra', 'deborah'], 'dick': ['richard'], 'dora': ['dorothea', 'dorothy', 'theodora'], 'dot': ['dorothea', 'dorothy', 'doris'], 'doug' : ['douglas'],
'ed': ['edward', 'edmund', 'edwin'], 'eddie': ['edward', 'edmund', 'edwin'], 'eddy': ['edward', 'edmund', 'edwin'], 'ella': ['eleanor', 'elinor', 'elizabeth', 'leonora', 
'ellen', 'isabel', 'isabella'], 'elsie': ['elizabeth', 'elisabeth'], 'eva': ['evelina', 'eveline', 'evelyn'], 'eve': ['evelina', 'eveline', 'evelyn'], 
'fanny': ['frances', 'francis', 'francesca'], 'franny': ['frances', 'francis', 'francesca'], 'fran': ['frances', 'francis', 'francesca'], 'flo': ['florence'], 
'francie': ['francis'], 'frankie': ['francis', 'frederica', 'francesca'], 'fred': ['frederic', 'frederick'], 'freddie': ['frederic', 'frederick'], 
'freddy': ['frederic', 'frederick'], 'gabe': ['gabriel'], 'gertie': ['gertrude'], 'gil': ['gilbert'], 'greg': ['gregory'], 'gus': ['augustus'], 
'hal': ['henry', 'harold'], 'harry': ['harold'], 'hatty': ['harriet', 'harriot'], 'hen': ['henry'], 'hugo': ['hugh'], 'izzy': ['isabel', 'isabella', 'isobel'], 
'jack': ['john'], 'jake': ['jacob'], 'jan': ['janet'], 'jean': ['jeanne', 'jeannette'], 'jeanie': ['jeanne', 'jeannette'], 'jeannie': ['jeanne', 'jeannette'], 'jeff' : ['jeffrey'],
'jen': ['jennifer'], 'jennie': ['jennifer'], 'jenny': ['jennifer'], 'jerry': ['jeremiah', 'jeremias', 'jeremy', 'gerald'], 'jess': ['jessica'], 'jessie': ['jessica'], 
'jim': ['james'], 'jimmie': ['james'], 'jimmy': ['james'], 'jo': ['joan', 'joanna', 'johanna', 'josephine'], 'joe': ['joseph'], 'joey': ['joseph'], 'johnnie': ['john'], 
'johnny': ['john'], 'jon': ['jonathan'], 'josh': ['joshua'], 'josie': ['josephine'], 'judy': ['judith'], 'jules': ['julia', 'juliet', 'julianne'], 
'julie': ['julia', 'juliet', 'julianne'], 'kate': ['katharine', 'katherine', 'kathleen'], 'kathy': ['katharine', 'katherine', 'kathleen'], 
'katie': ['katharine', 'katherine', 'kathleen'], 'ken': ['kenneth'], 'kit': ['catherine', 'catherina', 'katharine', 'katherine', 'kathleen'], 
'kitty': ['catherine', 'catherina', 'katharine', 'katherine', 'kathleen'], 'larry': ['laurence', 'lawrence'], 'len': ['leonard'], 'lenny': ['leonard'], 
'lex': ['alexa'], 'lexi': ['alexa'], 'libby': ['elisabeth', 'eliza', 'elizabeth'], 'lilly': ['lilian', 'lillian'], 'lily': ['lilian', 'lillian'], 
'lisa': ['elisabeth', 'eliza', 'elizabeth'], 'liz': ['elisabeth', 'eliza', 'elizabeth'], 'liza': ['elisabeth', 'eliza', 'elizabeth'], 
'lizzie': ['elisabeth', 'eliza', 'elizabeth'], 'lizzy': ['elisabeth', 'eliza', 'elizabeth'], 'lou': ['louis'], 'louie': ['louis'], 'lucy': ['lucia', 'lucinda'], 
'luke': ['lucas'], 'maddie': ['madison', 'madeline'], 'mag': ['margaret'], 'maggie': ['margaret'], 'manny': ['emmanuel', 'immanuel'], 'margie': ['margaret', 'marjorie'], 
'mark': ['marcus'], 'mat': ['matthew', 'matthias'], 'matt': ['matthew', 'matthias'], 'mattie': ['matilda', 'mathilda'], 'matty': ['matilda', 'mathilda', 'martha'], 
'meg': ['margaret', 'megan', 'meghan'], 'meggy': ['margaret', 'megan', 'meghan'], 'mick': ['michael'], 'micky': ['michael'], 'mike': ['michael'], 
'minnie': ['mary', 'miriam'], 'molly': ['mary', 'miriam'], 'nan': ['ann', 'anna', 'anne', 'hannah', 'annette', 'nancy'], 'nat': ['nathan', 'nathanael', 'nathaniel'], 
'ned': ['edward', 'edmund'], 'neddy': ['edward', 'edmund'], 'nell': ['eleanor', 'elinor', 'leonora', 'eleanore', 'helen'], 
'nellie': ['eleanor', 'elinor', 'leonora', 'eleanore', 'helen'], 'nic': ['nicholas', 'nicolas'], 'nick': ['nicholas', 'nicolas'], 
'nora': ['eleanor', 'elinor', 'leonora', 'eleanore'], 'norah': ['eleanor', 'elinor', 'leonora', 'eleanore'], 'ollie': ['oliver', 'olive'], 'olly': ['oliver', 'olive'], 
'pat': ['patrick', 'patricia'], 'patty': ['patricia'], 'peg': ['margaret'], 'peggy': ['margaret'], 'penny': ['penelope'], 'pete': ['peter'], 'phil': ['philip', 'phillip'], 
'polly': ['mary', 'miriam', 'pollyanna'], 'prue': ['prudence'], 'randy': ['rudolph', 'randolph'], 'ray': ['raymond', 'raymund'], 'reg': ['reginald', 'reynold'], 
'reggie': ['reginald', 'reynold', 'regina'], 'rick': ['roderick', 'roderic', 'richard'], 'rob': ['robert', 'rupert'], 'robby': ['robert', 'rupert'], 
'rod': ['roderick', 'roderic', 'rodger'], 'ron': ['ronald'], 'rosie': ['rosa', 'rosabel', 'rosabella', 'rosalia', 'rosalie', 'rosalind', 'rosanna'], 
'roxy': ['roxana'], 'rudy': ['rudolph'], 'sal': ['sarah', 'sara'], 'sally': ['sarah', 'sara'], 'sam': ['samuel'], 'sammy': ['samuel'], 'sanders': ['alexander'], 
'sandy': ['alexander', 'sandra'], 'sim': ['simon', 'simeon', 'simone'], 'sol': ['solomon'], 'sophie': ['sophia'], 'steve': ['stephen', 'steven'], 
'stevie': ['stephen', 'steven'], 'sue': ['susan', 'susanna', 'susannah', 'suzanne'], 'susy': ['susan', 'susanna', 'susannah', 'suzanne'], 
'suzie': ['susan', 'susanna', 'susannah', 'suzanne'], 'suzy': ['susan', 'susanna', 'susannah', 'suzanne'], 'tammy': ['tamara'], 
'ted': ['edward', 'theodore'], 'teddy': ['edward', 'theodore'], 'terry': ['theresa', 'teresa', 'terrence'], 'tilda': ['matilda', 'mathilda'], 
'tillie': ['matilda', 'mathilda'], 'tim': ['timothy'], 'tina': ['christina'], 'toby': ['tobiah', 'tobias'], 'tom': ['thomas'], 'tommy': ['thomas'], 
'tony': ['anthony', 'antony'], 'tracie': ['theresa'], 'vicky': ['victoria'], 'will': ['william'], 'willy': ['william'], 'winnie': ['winifred', 'winfred'], 
'zac': ['zachary'], 'zach': ['zachary'], 'zak': ['zachary'], 'zeke': ['ezekial', 'ezekiel']}


def match_first(p1, p2):
    ret = False
    p1 = p1.lower()
    p2 = p2.lower()
    if p1 == p2:
        ret = True
    elif p1 in nicknames:
        for potential_full_name in nicknames[p1]:
            if potential_full_name == p2:
                ret = True
    elif p2 in nicknames:
        for potential_full_name in nicknames[p2]:
            if potential_full_name == p1:
                ret = True
    else:
        ret = False
    return ret

# main matching function, finds and returns matches in list with each entry being ['comment about type of match', match_info_as_dict]
def match(hash_options, person_info, lnhash):
    # for every last name match
    return_matches = []
    backup_matches = []
    for potential_match in hash_options:
        # check if first names match, including nicknames
        first_match = False
        first_match = match_first(potential_match['First'], person_info['First'])
        # first name matches, check zips, cities, states, and employers
        if first_match == True:
            if potential_match['Zip'] == person_info['Zip']:
                return_matches.append(['Perfect match', potential_match])
            elif potential_match['City'] == person_info['City'] and potential_match['State'] == person_info['State']:
                return_matches.append(['Perfect match', potential_match])
            else:
                if str(potential_match['Employer']) != '' and str(potential_match['Occupation']) != '':
                    if fuzz.token_set_ratio(potential_match['Employer'].lower(), person_info['Employer'].lower()) >= 90 and potential_match['Employer'] != 'Not Employed':
                        if potential_match['State'] == person_info['State']:
                            return_matches.append(['Perfect match', potential_match])
                        else:
                            backup_matches.append(['Potential match: same employer', potential_match])
                    elif (fuzz.token_set_ratio(potential_match['Occupation'].lower(), person_info['Employer'].lower()) >= 90 or fuzz.token_set_ratio(potential_match['Occupation'].lower(), person_info['Occupation'].lower()) >= 90 or fuzz.token_set_ratio(potential_match['Employer'].lower(), person_info['Occupation'].lower()) >= 90) and potential_match['Occupation'] != 'Not Employed' and person_info['Occupation'] != 'Not Employed':
                        backup_matches.append(['Potential match: occupation', potential_match])
                elif potential_match['State'] == person_info['State']:
                    backup_matches.append(['Potential match: same state', potential_match])
            # catching for first name space
        else:
            if ' ' in person_info['First']:
                if fuzz.token_set_ratio(potential_match['First'].lower(), person_info['First'].lower()) >= 90:
                    backup_matches.append(['Potential match: first name has space', potential_match])

    #except:
         #   return_matches = ['Failed in matching', []]

    # if still no matches, do a few hail marys
    if len(return_matches) == 0:
        # if no potential matches
        if len(backup_matches) == 0:
            # check if first/last switched
            if person_info['First'].lower() in lnhash:
                for flipped_p_match in lnhash[person_info['First'].lower()]:
                    if match_first(flipped_p_match['Last'], person_info['First']) and flipped_p_match['First'].lower() == person_info['Last'].lower():
                        return_matches.append(['Potential match: first/last switched', flipped_p_match])
            # check if initials
            if len(person_info['First']) == 1 or (len(person_info['First']) == 2 and person_info['First'][1] == '.'):
                for initial_p_match in hash_options:
                    if initial_p_match['First'][0] == person_info['First'][0] and (initial_p_match['Zip'] == person_info['Zip'] or (initial_p_match['City'] == person_info['City'] and initial_p_match['State'] == person_info['State'])):
                        return_matches.append(['Potential match: first name in FEC is initial', initial_p_match])
            # last name has space, check just first part and check just second part
            if person_info['Last'].lower().split(' ')[0] != person_info['Last'].lower():
                if person_info['Last'].split(' ')[0].lower().strip() in lnhash:
                    for split_p_match in lnhash[person_info['Last'].split(' ')[0].lower()]:
                        if match_first(split_p_match['First'], person_info['First']) and split_p_match['Zip'] == person_info['Zip']:
                            return_matches.append(['Potential match: first/zip match, last name dif space: ' + person_info['Last'].split(' ')[0] + ' vs ' + person_info['Last'], split_p_match])
                if person_info['Last'].split(' ')[1].lower().strip() in lnhash:
                    for split_p_match in lnhash[person_info['Last'].split(' ')[1].lower()]:
                        if match_first(split_p_match['First'], person_info['First']) and split_p_match['Zip'] == person_info['Zip']:
                            return_matches.append(['Potential match: first/zip match, last name dif space: ' + person_info['Last'].split(' ')[1] + ' vs ' + person_info['Last'], split_p_match])
            # check appostrophe differences
            if person_info['Last'][0].lower() == 'o' or person_info['Last'][0].lower() == 'd':
                name_wo_ap = person_info['Last'].translate(str.maketrans('', '', string.punctuation)).lower()
                name_w_ap = name_wo_ap[0] + "'" + name_wo_ap[1:]
                if name_wo_ap in lnhash:
                    for ap_p_match in lnhash[name_wo_ap]:
                        if match_first(ap_p_match['First'], person_info['First']) and (ap_p_match['Zip'] == person_info['Zip'] or (ap_p_match['City'] == person_info['City'] and ap_p_match['State'] == person_info['State'])):
                            return_matches.append(['Potential match: appostrophe difference', ap_p_match])

                if name_w_ap in lnhash:
                    for ap_p_match in lnhash[name_w_ap]:
                        if match_first(ap_p_match['First'], person_info['First']) and (ap_p_match['Zip'] == person_info['Zip'] or (ap_p_match['City'] == person_info['City'] and ap_p_match['State'] == person_info['State'])):
                            return_matches.append(['Potential match: appostrophe difference', ap_p_match])
            #check dash differences
            if '-' in person_info['Last']:
                name_w_space = person_info['Last'].replace('-', ' ')
                name_only_first = person_info['Last'].split('-')[0]
                name_only_last = person_info['Last'].split('-')[1]
                if name_w_space in lnhash:
                    for dash_p_match in lnhash[name_w_space]:
                        if match_first(dash_p_match['First'], person_info['First']) and (dash_p_match['Zip'] == person_info['Zip'] or (dash_p_match['City'] == person_info['City'] and dash_p_match['State'] == person_info['State'])):
                            return_matches.append(['Potential match: hyphen difference', dash_p_match])

                elif name_only_first in lnhash:
                        for dash_p_match in lnhash[name_only_first]:
                            if match_first(dash_p_match['First'], person_info['First']) and (dash_p_match['Zip'] == person_info['Zip'] or (dash_p_match['City'] == person_info['City'] and dash_p_match['State'] == person_info['State'])):
                                return_matches.append(['Potential match: hyphen difference', dash_p_match])
                elif name_only_last in lnhash:
                        for dash_p_match in lnhash[name_only_last]:
                            if match_first(dash_p_match['First'], person_info['First']) and (dash_p_match['Zip'] == person_info['Zip'] or (dash_p_match['City'] == person_info['City'] and dash_p_match['State'] == person_info['State'])):
                                return_matches.append(['Potential match: hyphen difference', dash_p_match])

                
        else:
            return_matches = backup_matches
    return return_matches

# formats output csv with notes and vanids
def edit_output(matches, fec_person, person_num, output):
    print(matches)
    output.append(fec_person)
    if len(matches) > 1:
        output[person_num]['VANID'] = ''
        output[person_num]['Notes'] = 'Multiple possible matches: '
        all_perfect = True
        for match in matches:
            if match[0] != 'Perfect match':
                all_perfect = False
            output[person_num]['VANID'] += str(match[1]['VANID']) + ', '
            output[person_num]['Notes'] += str(match[1]['VANID']) + ': ' + match[0] + ' '
        output[person_num]['VANID'] = output[person_num]['VANID'][:-2]
        if all_perfect == True:
            output[person_num]['Notes'] = 'Multiple perfect matches'
    elif len(matches) == 1:
        if matches[0][0] != 'Failed in matching':
            output[person_num]['VANID'] = matches[0][1]['VANID']
            output[person_num]['Notes'] = matches[0][0]
        else:
            output[person_num]['VANID'] = 'Failed in matching'
            output[person_num]['Notes'] = 'Failed in matching'
    else:
        output[person_num]['VANID'] = 'Not in NGP'
        output[person_num]['Notes'] = 'Not in NGP'
    return output

# find the matches by caling match and edit_output, returns output to be exported to csv
def find_matches(people, fec_people, output):
    lnhash = {}
    print('\nLoading NGP data...')
    for person_num in range(len(people)):
        #check if in hash
        if people['Last'].iloc[person_num] != '' and people['First'].iloc[person_num] != '':
            if people['Last'].iloc[person_num].lower() not in lnhash:
                #not in hash
                lnhash[people['Last'].iloc[person_num].lower()] = [{'VANID': people['VANID'].iloc[person_num], 'Last': people['Last'].iloc[person_num], 'First': people['First'].iloc[person_num], 'City': people['City'].iloc[person_num], 'State': people['State/Province'].iloc[person_num], 'Zip': people['Zip/Postal'].iloc[person_num], 'Employer': people['Employer Name'].iloc[person_num], 'Occupation': people['Occupation'].iloc[person_num]}]
            else:
                lnhash[people['Last'].iloc[person_num].lower()].append({'VANID': people['VANID'].iloc[person_num], 'Last': people['Last'].iloc[person_num], 'First': people['First'].iloc[person_num], 'City': people['City'].iloc[person_num], 'State': people['State/Province'].iloc[person_num], 'Zip': people['Zip/Postal'].iloc[person_num], 'Employer': people['Employer Name'].iloc[person_num], 'Occupation': people['Occupation'].iloc[person_num]})
    print('\nFinding FEC matches...')
    for person_num in range(len(fec_people)):
        fec_person = fec_people.iloc[person_num]
        if person_num % 1000 == 0 and person_num > 0:
            print('Done person', person_num)
        if "'" not in fec_person['Last'] and ("-" not in fec_person['Last']) and len(fec_person['Last']) > 2 and fec_person['Last'][2] != '.':
            fec_person_ln = fec_person['Last'].translate(str.maketrans('', '', string.punctuation))
        else:
            fec_person_ln = fec_person['Last']
        if fec_person_ln.lower() in lnhash:
            hash_people = lnhash[fec_person_ln.lower()]
        else:
            hash_people = []
        match_result = match(hash_people, fec_person, lnhash)
        output = edit_output(match_result, fec_people.iloc[person_num].to_dict(), person_num, output)
    return output

# main parts of function
# instructions
print('\nThis program takes in an NGP export file and an FEC export file. It finds VANID matches for the people on the FEC list.')
print('The program will create a new FEC file with a VANID column and Notes column titled "fec_duplicates.csv"')

# import files and format
import_file = input("\nNGP export filename (include '.csv'): ")
ngp_people = pd.read_csv(import_file, dtype=str)
ngp_people = ngp_people.replace(np.nan, '', regex=True)
import_file = input("FEC export filename (include '.csv'): ")
fec_people = pd.read_csv(import_file, dtype = str)
if len(fec_people['Zip'][0]) > 5:
    fec_people['Zip'] = '0' + fec_people['Zip']
    fec_people['Zip'] = fec_people['Zip'].str[-9:]
    fec_people['Zip'] = fec_people['Zip'].str[0:5]
else:
    fec_people['Zip'] = '0' + fec_people['Zip']
    fec_people['Zip'] = fec_people['Zip'].str[-5:]

# do everything
output = find_matches(ngp_people, fec_people, [])

# export csv
with open('fec_duplicates.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output[0].keys())
    writer.writeheader()
    writer.writerows(output)