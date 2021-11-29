# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 15:36:24 2021

@author: Vladimir
"""

"""
Things that will be done...
For the DOE file
First copy and paste the text of the table of contents
Al the topics are at the letter. <name of topic> followed by description and contact
Use that information to find the substring and subsequent text that happens after it

Will want to also get the award ceiligns and amoutnhs and that is at the 
number. explanation
You ahve the program overview in blue texts
You have the organization, the topic, and subtopics

tableOfContents.txt has the full table of contents with each line representing either the agency, topic, or subtopic
topicDescriptions.txt has all the lines of text that includes the above...
"""
import csv

def stripPeriods(s):
    # This will remove all the periods at the end of a line thing...
    # We know that at mosot will have two digit numbers followed by a period, so if we look for periods after the fourth point, will be able to remove all the periods...
    dot_start = s[4:].find('.')
    if dot_start == -1:
        return s.strip()
    else:
        return s[0:dot_start+5].strip()
    
def findInstanceOfLine(listOfLines, line, starting_position):
    try:
        # There is a change that there is a repeat of the same type of line so you have to factor in the startingPosition value as a way 
        find_current_line = listOfLines[starting_position:].index(line)
    except ValueError:
        # If doesn't find it that means we have to do a partial match
        # Long lines will only break up into two lines at most when representing it.
        # Here what we do is look for a partial match. Does the current line of interest show up with at least a third of its text in the beginning of any of the lines? We also have to devide the length by 3 to get only teh first third of the text
        find_current_line = listOfLines[starting_position:].index([s for s in listOfLines[starting_position:] if s.startswith(line[0:int(len(line)/3)])][0])
    return find_current_line+starting_position
    
    

toc = "tableOfContents.txt"
topicInfo = "topicDescriptions.txt"

# Let's read in all of the lines of data and store them for table of contents
# Because I copied over a pdf file, there are going to be some special characters.
# It's best to just ignore those characters, so when an error happens here to try to read text, ignore.
# This will open a file, save it as inputTxt, and then I store all the lines in toc_lines
with open(toc,errors="ignore",encoding='UTF-8') as inputTxt:
    toc_lines = inputTxt.readlines()

# Remove all the period stuff...
toc_lines = [stripPeriods(the_line) for the_line in toc_lines]

# Let's read in the topicInfo now
# By the way, you need to interpret the letters as UTF-8 encoding. It's what the pdf files are typically read in as. It also allows for em-dashes the slightly longer dashes you see in a lot of writing. encoding refers to how all the characters are stored and there's several other ones, most notably ASCII which has far fewer characters to do stuff with.
with open(topicInfo,errors="ignore",encoding='UTF-8') as inputTxt:
    topicInfo_lines = inputTxt.readlines()
    
# Remove all of the lines that say  "Back to Table of Contents"
# Will do this by saying that we should get all the lines in the list only if that line is not equal to the above
# you can read the bracketted area as a sentence, give me those_stirngs for those_strings that are in the list if those_strings is not equal to something specific.
topicInfo_lines = [those_strings for those_strings in topicInfo_lines if those_strings != 'Back to Table of Contents\n']
# Now remove the last character in each of the lines for both because we do not want to deal with new line characters. Also remove all whitespace as well before and after (will be added at the end anyway)
toc_lines = [the_string[0:len(the_string)-1].strip() for the_string in toc_lines]
topicInfo_lines = [the_string[0:len(the_string)-1].strip() for the_string in topicInfo_lines]

# To store values, I am preallocating them here in case there is some issue where code tries to put it in there thus crfeating a blank.
current_department = ''
current_topic = ''
current_subtopic = ''
department_description = ''
topic_description = ''
subtopic_description = ''
max_phase1 = ''
max_phase2 = ''
accept_SBIR_Phase1 = ''
accept_STTR_Phase1 = ''
contact_name = ''
contact_email = ''

header = ['Department','Department Description','Topic','Topic Description','Subtopic','Subtopic Description','Max Phase 1','Max Phase 2','Accept SBIR Phase 1','Accept STTR Phase 1','Contact Name','Contact Email']
f = open('DOE_Topic_Descriptions_2022_Release2.csv', 'w', newline='\n',encoding='UTF-8')
writer = csv.writer(f)
writer.writerow(header)

# Because there are a lot of lines that have the same lettering like c. Other we have to have a variable that keeps track of how far we have gone down the list looking for the next section. 
topic_line_index = 0

for toc_index in range(len(toc_lines)):
    current_toc_line = toc_lines[toc_index]
    # Figure out if it's a department, topic, or subtopic
    if current_toc_line.find('OVERVIEW') >= 0:
        # Find location of first period and keep only the stuff to the left
        dot_position = current_toc_line.find('.')
        # Wherever overview is, go two to the right (': ', or ' -') and remove the spaces around it. Remeember to factor in the length of overview which is eight characters, so 10 total characters forward
        overview_position = current_toc_line.find('OVERVIEW')
        current_department = current_toc_line[overview_position+10:dot_position].strip()
        
        # To get the description here keep going until you hit the next line...
        # First get the position of where the initial line is...
        find_current_line = findInstanceOfLine(topicInfo_lines, current_toc_line,topic_line_index)
        topic_line_index = find_current_line
        find_next_line = findInstanceOfLine(topicInfo_lines, toc_lines[toc_index+1],topic_line_index)
        topic_line_index = find_next_line
        # Now get all the text from the line after that first to the ones right until the next (not including next). Put a space in front of all of these
        department_description = ' '.join(topicInfo_lines[find_current_line+1:find_next_line])
        
    else:
        # Find where the first period occurs, and get everything to the left
        dot_position = current_toc_line.find('.')
        # Save the part to the left to determine if letters or numbers. go from beginning (0) to 1 before dot_position
        # In python, the positions start at 0 and the last position listed is not included
        to_left = current_toc_line[0:dot_position]
        # Now just get the title by getting all the text in between the two dots, replace any dots with spaces, and remove all spaces
        just_title= current_toc_line[dot_position+1:].replace('.',' ').strip()
       
        if to_left.isalpha():
            current_subtopic = just_title
            # Each subtopic should end with a questions section before the next one which has contact information
            # After each of these subtopics, we should store the data in a new row on an excel sheet or the like
            
            # First get the location of this topic and the next one...
            find_current_line = findInstanceOfLine(topicInfo_lines, current_toc_line,topic_line_index)
            topic_line_index = find_current_line
            
            if toc_index+1 < len(toc_lines):
                find_next_line = findInstanceOfLine(topicInfo_lines, toc_lines[toc_index+1],topic_line_index)
                topic_line_index = find_next_line
            else: # It should jsut be the end...
                find_next_line = len(topicInfo_lines)
            
            # Now that we have the beginning and ending, let us look within there to find the specific occurrence of Questions - Contact
            lines_involved = topicInfo_lines[find_current_line+1:find_next_line]
            # Now figure out where questions occurrs
            question_index = lines_involved.index([s for s in lines_involved if s.startswith('Questions – Contact')][0])
            question_line = lines_involved[question_index]
            # Extract out the name and the email from that line
            # Just look for occurrence of : and , and then go two after : to skip space and the :, and don't have to subtract on the , character because it will stop before there
            # Check if it's name then comma then email format, if not do other
            if question_line.find(',') == -1:
                contact_name = 'None Provided'
                contact_email = question_line[question_line.find(':')+2:]
            else:
                # Check to see if two names...Put in a .gov and because there are cases where or is said but also and. We want the times where it's just two names listed
                if question_line.find('.gov and ') >= 0:
                    question_line = question_line[question_line.find(':')+2:]
                    contact_name = '';
                    contact_email = '';
                    for name_email in question_line.split(' and '):
                        contact_name += name_email[0:name_email.find(',')]+';'
                        contact_email += name_email[name_email.rfind(',')+2:]+';'
                    contact_name = contact_name[0:-1] # Take off the last semicolon
                    contact_email = contact_email[0:-1]
                else:
                    # there is one more case where they say or
                    if question_line.find(' or ') >= 0:
                        # Get after the colon
                        question_line = question_line[question_line.find(':')+2:]
                        contact_name = '';
                        contact_email = '';
                        for name_email in question_line.split(' or '):
                            contact_name += name_email[0:name_email.find(',')]+';'
                            contact_email += name_email[name_email.rfind(',')+2:]+';'
                        contact_name = contact_name[0:-1] # Take off the last semicolon
                        contact_email = contact_email[0:-1]
                    else:
                        contact_name = question_line[question_line.find(':')+2:question_line.find(',')]
                        contact_email = question_line[question_line.rfind(',')+2:]
                
            # Now combine all the lines of interest excluding question...
            subtopic_description = ' '.join(lines_involved[0:question_index])
            
            # Now say all the values in the Excel sheet...
            writer.writerow([current_department,department_description,current_topic,topic_description,current_subtopic,subtopic_description,max_phase1,max_phase2,accept_SBIR_Phase1,accept_STTR_Phase1,contact_name,contact_email])
        else:
            current_topic = just_title
            # The first two lines after the current_topic have information like maximum and the like that we need to process
            # Use the same logic as used in current_toc line except we have to process the first two lines as well..
            find_current_line = findInstanceOfLine(topicInfo_lines, current_toc_line,topic_line_index)
            topic_line_index = find_current_line
            
            # Need to check that it starts at maximum otherwise the topic line was split because it was too long
            # Increase by one and should be good
            while topicInfo_lines[find_current_line+1].startswith('Maximum Phase I Award Amount: ') is False:
                find_current_line += 1
            
            # Now get the data from the next two lines for the maximum and stuff. If we just split each line into spaces we can just count 6th and 12th one (5th and 11th if we started counting at 0 instead of 1 like Python)
            #Maximum Phase I Award Amount: $200,000 Maximum Phase II Award Amount: $1,100,000
            line_split = topicInfo_lines[find_current_line+1].split(' ')
            max_phase1 = line_split[5]
            max_phase2 = line_split[11]
            #Accepting SBIR Phase I Applications: YES Accepting STTR Phase I Applications: NO
            line_split = topicInfo_lines[find_current_line+2].split(' ')
            accept_SBIR_Phase1 = line_split[5]
            accept_STTR_Phase1 = line_split[11]
            
            # Now get the next lien for joining
            find_next_line = findInstanceOfLine(topicInfo_lines, toc_lines[toc_index+1],topic_line_index)
            topic_line_index = find_next_line
            # Now get all the text from the line after that first to the ones right until the next (not including next). Put a space in front of all of these
            topic_description = ' '.join(topicInfo_lines[find_current_line+3:find_next_line])

f.close()