#Emma Stavis
#7/2022
#NOTE!! This code was written for a campaign. In order for future users' ease, this code was written to prioritize making it intuitive over optimized 

import requests
import bs4
import pandas as pd
MIN_DONATION = 500 # the threshold for contributions to include

# load_data: for every person in given df names, forms query url, requests, and scrapes page to load data into personal_data list
    # calls parse_data on personal_data list to process further
def load_data(names, include_candidates):
    
    baseurl = 'https://www.opensecrets.org/donor-lookup/results?name='

    #For every person (row) in df names, create url, query, and add data to temporary array
    for person_num in range(len(names)): 
        skip = False
        personal_data = []

        #Make url and query for the person
        url = baseurl + names.iloc[person_num, names.columns.get_loc('Name')] + '&order=desc&sort=D'
        filters = ['Zip', 'State', 'Cycle', 'Employ', 'Jurisdiction', 'Cand', 'Type']
        new_baseurl = url
        new_baseurl = new_baseurl + '&' + filters[0].lower() + '=' + str(names.iloc[person_num, names.columns.get_loc(filters[0])])[0:5]
        for i in range(6):
            new_baseurl = new_baseurl + '&' + filters[i+1].lower() + '='
        response = requests.get(new_baseurl)
        try:
            souppre = bs4.BeautifulSoup(response.text, features= 'html.parser')
        except: 
            names.iloc[person_num, names.columns.get_loc('Research')] = 'Failed in search'
            skip = True

        #Add all the rows for the individual (if there are results) on open secrests to personal_data 
        if skip != True:
            more_pages = True
            page_num = 0
            while (more_pages == True and page_num < 11):
                if page_num != 0:
                    page_url = new_baseurl + '&page=' + str(page_num) 
                else:
                    page_url = new_baseurl
                response = requests.get(page_url)
                souppre = bs4.BeautifulSoup(response.text, features= 'html.parser')
                #to inpsect soup if needed
                with open('htmlstuff.txt', 'w') as f:
                    f.write(str(souppre))
                try:
                    soup = souppre.find('tbody') #find table
                    rows = soup.find_all('tr') #find rows
                    for row in rows:
                        tds = row('td')
                        cells = []
                        for td in tds:
                            cells += td.contents
                        if not '<div style="width: 45%' in str(cells): #some weird divider thing to avoid
                            personal_data.append(cells)
        
                except:
                    break
                
                if(page_num == 0):
                    page_num += 2
                else:
                    page_num += 1

            #Parse data for that person
            parse_data(personal_data, person_num, names, include_candidates) 

            print('Done person', person_num)

"""----------------------------------------------------------------------------------
HELPER FUNCTIONS for PARSE_DATA and PARSE_DATA
----------------------------------------------------------------------------------"""

 # strip_term: deletes extra characters and spaces from terms. 
    # Returns that element
def strip_term(row, i, j):
    row[i] = str(row[j]).strip("[]'")
    row[i] = str(row[j]).strip()
    return row[i]   

# increment: increments i and j
    # Returns i and j in tuple
def increment(i, j): 
    i += 1 #index of where we put it, just keeps going as normal
    j += 1 #index of information we want
    return [i, j] 

# expected: checks to see if next term in data is category we are expecting
    # returns true or false accordingly
def expected(row, i, j): 
    date_chars_and_money = "0123456789-$"
    date_chars = "0123456789-"
    dashes = '-'

    #If it should be an occupation, makes sure it has word-characters (not an amount or date). If it's all dashes, just keep.
    if i == 3:
        if (not all([chars in date_chars_and_money for chars in row[j]])) or all([chars in dashes for chars in row[j]]): 
            return True 
        else:
            return False

    #If it should be a date, make sure it has only date characters
    elif i == 4:
        if (all([chars in date_chars for chars in row[j]])):
            return True
        else:
            return False
    
    #If it should be an amount
    elif i == 5:
        try:
            row[j][0] == '$'
            return True
        except:
            return False
    
    #If it should be a candidate or jurisdiction
    elif i == 6 or i == 7:
        try:
            x = str(row[i])
            return True
        except:
            return False
    else:
        return True


# pass_filters: checks if a given subsection of a contribution entry is valid
    # if it is a date, check if it's 2018 or later
    # if it is an amount, check if it is > MIN_DONATION or in include_candidates
    # returns number accordingly
def pass_filters(contribution_entry, i, include_candidates):

    
    try:
        #If date and before 2018 or not an int, don't keep
        if i == 4 and int(contribution_entry[i][-4:]) < 2018: 
            return -1
        #If amount, check if < MIN_DONATION and not in include candidates
        elif i == 6:
            if contribution_entry[5][0] == '-': #negative number, don't include
                return -1
            amount_as_float = contribution_entry[5][1:].replace(',', '')
            amount_as_float = float(amount_as_float)
            if (amount_as_float < MIN_DONATION and contribution_entry[i] not in include_candidates): #keep to sum and see if anything is big enough
                return -2
            else:
                return 0
        #Keep
        else: 
            return 0
    except:
        print('There was an exception and an entry was deleted to avoid crashing. Check this person to double check data retieved. Contribution deleted: ')
        print(contribution_entry)
        return -1
    
    


# format_name: checks to see if os_name (the open secrets-formatted name that is a key in year_data) is in include_candidates
    # if it is, format that contribution entry with readable_name in include_candidates
    # otherwise, if name has a comma and '(D)', format name so it is first last
    # returns string that looks like: Joe Biden $3000
def format_name(os_name, year_data, include_candidates):
    #Format amount given to that candidate
    amount = str(int(year_data[os_name])) + '; '

    #If candidate in include candidates, format as in that dictionary (which was made from the inputted csv)
    if (str(os_name).lower() in include_candidates):
        cand_name = include_candidates[str(os_name).lower()]
    
    else:
        #If it is formatted like a regular name, i.e. with a comma and (D), format as regular name
        if '(D)' in str(os_name) and ',' in str(os_name):
            key_parts = str(os_name).split(',')
            cand_name = key_parts[1][:len(key_parts[1]) - 4] + ' ' + key_parts[0]
        #If a weird candidate name format or something like a PAC with no comma and (D), format as-is
        else:
            cand_name = str(os_name)

    #Return string that looks like: Joe Biden $4000;
    return cand_name + ' $' + amount


# sum_and_summary: used in compile_research to sum an individual's contributions to candidates in one year and format nicely using format_name
    # failed_flag == 1 signifies the contribution_data being passed in are failed data, i.e. < $2000 and not candidates of interest. This means, once summed,
    # this function will check whether summed contributions exceed $2000 or not

    # failed_flat == 0 signifies that contribution_data are "good" entries and just need to be processed and formatted
    # returns research_data, a dictionary where keys are years and values are the string of research for that year

def sum_and_summary(contribution_data, include_candidates, failed_flag):
    # now, we go by entry, keeping running totals per year of contributions to candidates
    entry_num = 0
    #No data for that person :(
    if(contribution_data == []):
        return {}
    
    current_year = contribution_data[0][4][-4:]
    research_data = {} # year : year's research string, e.g. 2022 : '2022: Joe Biden $3000; Fetterman $4000'
    year_data = {} # candidate : amount, e.g. 'Biden, Joe (D)' : 3000

    #Go through each entry, adding information to year_data dictionary where key:value is candidate:amount.
        # Amounts for each candidate are summed
        
    while entry_num < len(contribution_data):
        entry_year = contribution_data[entry_num][4][-4:]

        # When we get to new year, compile year_data into year_string and make value for created research_data key that is that year
        if current_year != entry_year:
            year_string = str(current_year) + ': '
            for key in year_data:
                if failed_flag == 0 or (failed_flag == 1 and year_data[key] >= MIN_DONATION):
                    year_string += format_name(key, year_data, include_candidates)
            if year_string != str(current_year) + ': ':
                year_string = year_string[:len(year_string) - 2] + '  ||  '
                research_data[current_year] = year_string
            current_year = entry_year
            year_data = {}
        
        #Add entry to year_data[candidate] after formatting number correctly
        candidate = contribution_data[entry_num][6]
        if '-' in contribution_data[entry_num][5]:
            number_to_add = '-' + contribution_data[entry_num][5][-(len(contribution_data[entry_num][5]) - 2):]
        else:
            number_to_add = contribution_data[entry_num][5][-(len(contribution_data[entry_num][5]) - 1):]
        if ',' in number_to_add:
            number_to_add = number_to_add.replace(',', '')
        if candidate not in year_data:
            year_data[candidate] = float(number_to_add)
        else:
            year_data[candidate] += float(number_to_add)
        entry_num += 1

    #We still need to add last year's data to year_string and then year_string to research_data dictionary
    year_string = str(current_year) + ': '
    for key in year_data:
        if failed_flag == 0 or (failed_flag == 1 and year_data[key] >= MIN_DONATION):
            year_string += format_name(key, year_data, include_candidates)
    if year_string != str(current_year) + ': ':
        year_string = year_string[:len(year_string) - 2] + '  ||  '
        research_data[current_year] = year_string
    
    #Return research_data, which should have key:value pairs like: 2022 : '2022: Joe Biden $3000; Fetterman $4000'
    return research_data


# compile_research: takes in personal data (>$2000 entries and candidates of interest entries) and failed_data (the rest of the person's data)
    # sums contributions to candidates per year and formats them nicely using sum_and_summary
def compile_research(personal_data, include_candidates, failed_data):
    #Make dictionaries with year : formatted string of research for that year
    reg_data = sum_and_summary(personal_data, include_candidates, 0) 
    failed_data_to_include = sum_and_summary(failed_data, include_candidates, 1) 
    
    #Adds together the two dictionaries from above, i.e. if failed_data had any data that surpassed $2000 when summed
    for key in failed_data_to_include: 
        if key in reg_data:
            reg_data[key] = reg_data[key][:len(reg_data[key]) - 6] + failed_data_to_include[key][5:]
        else:
            reg_data[key] = failed_data_to_include[key]
    
    #compile the whole string of research
    research_string = '' 
    for key in reg_data: 
        research_string += reg_data[key]
    return research_string


# parse_data: takes in messy list of an individual's data and cleans it up
    # for every row, deletes if bad row, and otherwise cleans and formats data using expected, strip_term, pass_filters and increment functions
    # then, uses compile_reserach to compile research into a nice string 
    # adds entry in research column in names with that compiled string, or 'No giving history' if there were no results
    # no return, just modifies names

def parse_data(personal_data, person_num, names, include_candidates): #organize data nicely FOR A GIVEN PERSON

    #ADD CONDENSED INFO FROM personal_data TO RESEARCH COLUMN IN NAMES
    row_num = 0
    failed_data = []
    while row_num < len(personal_data):  #for each row
        
        #If weird row, delete
        row_deleted = False
        if len(personal_data[row_num]) == 1: 
            personal_data.pop(row_num)
            continue
        
        #If normal row, parse each cell, and organize
        if len(personal_data[row_num]) > 4: 
            i = 0
            j = 0
            while i < len(personal_data[row_num]):
                #If entry is weird break thing, delete it
                if str(personal_data[row_num][i]) == '<br/>':
                    personal_data[row_num].pop(i)

                #If entry matches as expected, i.e. if we're expecting a date and got a date
                elif expected(personal_data[row_num], i, j): 
                    
                    #Strip term
                    personal_data[row_num][i] = strip_term(personal_data[row_num], i, j)
                    
                    #filter: return 0 if pass, -1 if too old, -2 if <min_donation not candidate of interst
                    failed_return = pass_filters(personal_data[row_num], i, include_candidates) 

                    #Need to check if sum of contributions > min_donation later, so put in failed_data for now but take out of personal_data
                    if failed_return == -2: 
                        failed_data.append(personal_data[row_num])
                        personal_data.pop(row_num)
                        row_deleted = True
                        break
                    
                    #Too old, delete row
                    elif failed_return == -1: 
                        personal_data.pop(row_num)
                        row_deleted = True
                        break
                    
                    #Good entry, keep in personal_data and icnrement to next cell in row
                    else: 
                        i, j = increment(i, j)

                #If it is not what we expected (which means we're missing occupation, date etc.)
                else: 
                    personal_data[row_num].insert(i, '') #add empty column in row
                    i, j = increment(i, j) #keep going to next cell that should be as expected

            #If we didn't delete the row, increment the row number
            if row_deleted == False: 
                row_num += 1
 
    #BY HERE, WE SHOULD HAVE ALL DATA WE WANT IN ROWS IN PERSONAL DATA, DATA THAT DID NOT PASS IN FAILED_DATA
    if personal_data != []:
        research_string = compile_research(personal_data, include_candidates, failed_data)
    else:
        research_string = ''
    if research_string == '':
        names.iloc[person_num, names.columns.get_loc('Research')] = 'No giving history' #add this to the person's row
    else:
        names.iloc[person_num, names.columns.get_loc('Research')] = research_string #add all of that research to the person's row

"""----------------------------------------------------------------------------------
HELPER FUNCTION for MAIN to organize data
----------------------------------------------------------------------------------"""

# organize: organizes incoming dataframe names to be usable
    # returns names and flag that it worked
def organize(names):

    #Change zip and state columns as necessary
    if 'Zip/Postal' in names.columns:
        names = names.rename(columns={'Zip/Postal':'Zip'})
    if 'State/Province' in names.columns:
        names = names.rename(columns={'State/Province': 'State'})
    if not ('Zip' in names.columns and 'State' in names.columns and 'First' in names.columns and 'Last' in names.columns):
        return [names, False]

    #Format zip to make sure is 5 numbers including leading 0 if applicable
    names['Zip'] = '0' + names['Zip']
    names['Zip'] = names['Zip'].str[-5:]

    #Create new columns and format Name to be First+Last in order to search more easily later
    names['Name'] = ''
    names['Research'] = ''
    for row in range(len(names)):
        first_string = str(names['First'].iloc[row])
        last_string = str(names['Last'].iloc[row])
        if first_string != '' and last_string != '': 
            names.iloc[row, names.shape[1] - 2] = first_string + '+' + last_string
        else:
            names.drop(names.index[row])
    
    #Delete other column
    return [names, True]


"""----------------------------------------------------------------------------------
MAIN PROGRAM
----------------------------------------------------------------------------------"""

# main: takes in information, reads csv and formats slightly
    # calls load_data which calls all other functions
    # re-formats and exports
def main():
    #Instructions and get inputs
    print("\nInstructions: ")
    print("1. Type in filename of a csv with columns 'First', 'Last', 'Zip' or 'Zip/Postal', and 'State' or 'State/Province'")
    print('2. Then, type in the name of a csv with candidates for whom to includea ll donations.')
    print('\nProgram will export file entitled research.csv with same columns and research that includes all entries >$2000 and all contributions to specified candidates.\n')
    print('DISCLAIMERS:')
    print('- The program searches by zipcode, so if the zipcode is wrong, no entries will show. Do a human-check if an entry seems off.')
    print('- The program also uses the candidate file inputted to filter, so make sure all names are included and formatted as they appear in Open Secrets.')
    print('- If the run fails, double check that column names are exact and try exporting the spreadsheet to a csv differently (make sure NOT to just convert a Numbers file). If it gets stuck on one person, quit and restart the program.')
 
    print('- To change monetary criterion, change "MIN_DONATION" at top of the code.\n')
    print('-------------STARTING-------------\n')
    
    import_file = input("Filename with list of people (include '.csv'): ")
    initial_candidates = input("Filename with candidates of interest (include '.csv'): ")

    #Read and format include_candidates into a dictionary for easier use
    names = pd.read_csv(import_file, dtype=str)
    initial_candidates = pd.read_csv(initial_candidates)
    for i in range(len(initial_candidates['os_names'])):
        initial_candidates['os_names'].iloc[i] = initial_candidates['os_names'].iloc[i].lower()
    include_candidates = {}
    for i in range(len(initial_candidates['os_names'])):
        include_candidates[initial_candidates['os_names'].iloc[i]] = initial_candidates['readable_names'].iloc[i]

    #Organize columns
    organized = organize(names)
    names = organized[0]
    if organized[1] == False:
        print('Column name error. Please try running again after checking column names.')
        return

    #Do all the work
    load_data(names, include_candidates) 

    #Reorganize
    del names['Name']
    names = names.rename(columns={'State':'State/Province', 'Zip': 'Zip/Postal'})

    #Export to csv
    names.to_csv(import_file[:len(import_file)-4] + '_'+ 'researched.csv', index = False)
    
if __name__ == "__main__":
    main()

