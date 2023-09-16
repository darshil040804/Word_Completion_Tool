###########################################################################################
# Word_Databse_Completion_Tool
#
# ALGORITHM
# 
# This project uses 4 functions to filter out the words with a specific prefix
# open_file(): This function keeps asking the user for a filename until valid 
# filename is entered. Then it opens the file entered.
# read_file(): This function reads through each word of the opened file and
# returns a set of all these words 
# fill_completions: This function creates a dictionary of the form 
# {(i,ch): set(word1,word2...etc)} and returns it. Here i is the index of each 
# word in the main set and ch is the character at index i of the word that is being addressed
# and the set is the set of words containing character "ch" at index "i".
# find_completions: This function uses the intersection functionality and returns a set of
# words that contain the prefix entered by the user
# Now the main function asks the user to enter a prefix and then prints all the words
# having that prefix seperated by commas
#
##############################################################################################

import string   #to use string.punctuation

def open_file():
    '''
    This function prompts the user to enter a vocabulary file name.
    It keeps prompting the user for the filename until a valid file
    name is entered. Then it opens the file with UTF-8 encoding and
    returns the file pointer fp. 
    '''

    #while loop to keep prompting for filename untill valid filename entered
    while True:
        #try-except suite to check if the entered filename exists. 
        try:
            filename = input("\nInput a file name: ")
            fp = open(filename, encoding = 'UTF-8')
            return fp
            break   #break while loop if file is opened.
        except FileNotFoundError:
            print("\n[Error]: no such file")    #print error message if file is not found


def read_file(fp):
    '''
    This function reads the opened file. It then creates a a set of
    all words in that file. However, it ignores the words with one letter 
    only and removes all the punctuations from words that contain puncations
    like "'","-",etc. Finally, it returns the set of all words.  
    '''
    words_set = set()

    #for loop to iterate over each line in the file
    for line in fp:
        line = line.strip()    #stripping off any new line characters.
        line_list = line.split()    #making a list of all words in a line

        #for loop to iterate over each word in the list created above
        for word in line_list:
            word = word.strip(string.punctuation)   #getting rid of any punctuations within words
            word = word.lower()     #converting all words to lowercase

            #filtering out the words with that are alphabetical and have more than one character
            if word.isalpha() and len(word) >1:
                words_set.add(word)
    return words_set


def fill_completions(words):
    '''
    This function creates a dictionary that stores a set of words as completions
    for each character at each index of a word in the set of words. The keys of 
    this dictionary are of the form (i,ch) where i is the index and ch is the 
    character at that particular index of the word being adressed. The corresponding 
    values of this dictionary are a set of words that have thr character "ch" at index "i".
    '''
    word_dic = {}

    #for word to iterate over each word in thw words set
    for word in words:

        #for loop to iterate over each character in a word
        for i in range(len(word)):
            ch = word[i].lower()    

            #if condition to check if the (i,ch) tuple exists as a key in the word_dic
            if (i,ch) not in word_dic.keys():
                word_dic[(i,ch)] = set()    #if key does not exist, set the value of that key as an empty set
            word_dic[(i,ch)].add(word)   #Add each word to the set of words corresponding to the key (i,ch)
    return word_dic


def find_completions(prefix,word_dic):
    '''
    This function takes a prefix and a completions dictionary of the form 
    {(i,ch): set(word1,word2...etc)}. Return the set of words in the 
    completions dictionary that complete the prefix, if any. If the prefix 
    cannot be completed to any vocabulary words, return empty set. 
    '''
    completions_set = set()
    prefix = str(prefix.lower()) 

    #for loop to iterate over each character in the prefix
    for i in range(len(prefix)):

        '''if a word having the same character at the same index as that of prefix
        is present in the word_dic, interesect it with the completions set.'''
        if (i,prefix[i]) in word_dic.keys():
            if i==0:
                completions_set = word_dic[(i,prefix[i])]                
            else:
                #intersection of each set with completions_set to fetch all words with the exact, desired prefix.
                completions_set = completions_set.intersection(word_dic[(i,prefix[i])])
        else:
            return set()    #return empty set if no words found with the entered prefix
    return completions_set

def main():   
    '''
    This is the main function that is used to interact with the user. It 
    asks the user to enter a prefix and prints all the words containing that
    prefix seperated by commas. It alspo prints a "no complletions" message if
    no words with the entered prefix are found. Lastly, it prints the exiting
    message when the user chooses to quit the program.
    '''
    #calling open_file() function to open a file    
    fp = open_file()       
    #calling read_file function to get the set of all words in the opened file
    words_set = read_file(fp)   
    #calling the fill_completions function to get the main dictionary {(i,ch): set(word1,word2...etc)}.
    word_dic = fill_completions(words_set)

    while True:     #main loop to keep asking for prefix 
        prefix = input("\nEnter a prefix (# to quit): ")

        #if condition to exit loop as per the user's requirements
        if prefix == "#":
            print("\nBye")
            break
        else: 

            #calling the find_completions function to get the set of words containing the entered prefix
            completions_set = find_completions(prefix,word_dic)

            #if condition to check if the completions_set is empty or not
            if completions_set != set():
                helper_list = list(completions_set) #convert completions_set to list
                helper_list.sort()  #sort the helper_list obtained

                #creating a word string with all words seperated by commas
                words_string = ", ".join(helper_list)
                print("\nThe words that completes {} are: {}".format(prefix,words_string))
            else:
                print("\nThere are no completions.")    #print no completions message if no words found
        

if __name__ == '__main__':
    main()
