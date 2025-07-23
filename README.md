
# ATLANTIC DESCRIPTION PARSER
For use in Land Surveying Field-to-Finish processing. 
## USE
I created this application to help standardize the point descriptions in point files created in the field. The point files is a comma seperated file with 5 columns The last of which is the description field. It processes the point file in two stages.
- Replacement phase: This application itterates through each line and compares the first two words in the last colunm with a dictionary of key, value pairs. The key holds the most frequently used non standard code and the value holds the standard code. This process substitutes the non standard code with the standard code. The substitution dictionary is stored as a json file. This produces a file name "preprocessed_{file_name}.{ext}"  
- Format phase: In the second phase the format of the code is check for field to finish formating and reformats the description if needed. For example the property corner codes require the following format: code space /size. This produces a file {file}_processed.{ext}.
