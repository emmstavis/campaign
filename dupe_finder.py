#Emma Stavis
#7/2022
#NOTE!! This code was written for Fetterman for PA. In order for future users' ease, this code was written to prioritize making it intuitive over optimized 

import pandas as pd
from fuzzywuzzy import fuzz
import csv

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

def match(hash_options, person_info):
    # for every last name match
    for potential_match in hash_options:
        # check if first names match
        first_match = False
        try:
            if potential_match['First'] == person_info['First']:
                first_match = True
            elif potential_match['First'].lower() in nicknames:
                for potential_full_name in nicknames[potential_match['First'].lower()]:
                    if potential_full_name == person_info['First'].lower():
                        first_match = True
            elif person_info['First'].lower() in nicknames:
                for potential_full_name in nicknames[person_info['First'].lower()]:
                    if potential_full_name == potential_match['First'].lower():
                        first_match = True 
            # if first matches, see if other stuff matches
            if first_match == True:
                if potential_match['Zip/Postal'] == person_info['Zip/Postal']:
                    return [0, potential_match]
                elif (fuzz.token_set_ratio(potential_match['Address'].lower(), person_info['Address'].lower()) >= 90) or (fuzz.partial_ratio(potential_match['Address'].lower(), person_info['Address'].lower()) >= 90):
                    return [0, potential_match]
                elif (potential_match['PreferredEmail'] == person_info['PreferredEmail'] and person_info['PreferredEmail'] != 'info@johnfetterman.com') or potential_match['Cell Phone'] == person_info['Cell Phone'] or potential_match['Home Phone'] == person_info['Home Phone']:
                    return [0, potential_match]
        except:
            return [-1, '']
    return [1, '']


    
def find_dupes(people, output):
    lnhash = {}
    for person_num in range(len(people)):
        if person_num%5000 == 0:
            print('Done person',person_num)
        #check if in hash
        if people['Last'].iloc[person_num] not in lnhash:
            # Last name not in hash
            lnhash[people['Last'].iloc[person_num]] = [{'VANID': people['VANID'].iloc[person_num], 'Last': people['Last'].iloc[person_num], 'First': people['First'].iloc[person_num], 'Home Phone': people['Home Phone'].iloc[person_num], 'Cell Phone': people['Cell Phone'].iloc[person_num], 'PreferredEmail': people['PreferredEmail'].iloc[person_num], 'Address': people['Address'].iloc[person_num], 'City': people['City'].iloc[person_num], 'State/Province': people['State/Province'].iloc[person_num], 'Zip/Postal': people['Zip/Postal'].iloc[person_num]}]
        else:
            # see if there's a match in hash
            match_result, matched_person = match(lnhash[people['Last'].iloc[person_num]], people.iloc[person_num].to_dict())
            if match_result == 0: # if a match, add both people to running dupes
                output.append(matched_person)
                output.append(people.iloc[person_num].to_dict())

            # if we are here, there was no match, so append to that value in hash :(
            elif match_result == 1:
                lnhash[people['Last'].iloc[person_num]].append({'VANID': people['VANID'].iloc[person_num], 'Last': people['Last'].iloc[person_num], 'First': people['First'].iloc[person_num], 'Home Phone': people['Home Phone'].iloc[person_num], 'Cell Phone': people['Cell Phone'].iloc[person_num], 'PreferredEmail': people['PreferredEmail'].iloc[person_num], 'Address': people['Address'].iloc[person_num], 'City': people['City'].iloc[person_num], 'State/Province': people['State/Province'].iloc[person_num], 'Zip/Postal': people['Zip/Postal'].iloc[person_num]})
    return output

# intake file
import_file = input("NGP export filename (include '.csv'): ")
people = pd.read_csv(import_file, dtype=str)

output = []
output = find_dupes(people, output)
with open(import_file[:-4] + '.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=people.keys())
    writer.writeheader()
    writer.writerows(output)
print("Written export file: " + import_file[:-4] + '.csv')