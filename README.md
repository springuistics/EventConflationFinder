# EventConflationFinder
Analyzes text, finds and counts satellite-framed and verb-framed expressions in English (as of 10/28/2022) and Japanese (coming soon). 

The tool distinguishes between motion and change-of-state expressions and further flags expressions that are instances of path reduplication (Spring & Ono, 2014) and expressions that the tool is unsure about. 

Counts, items, and example sentences for checking are output by the tool.

Currently (as of 10/28/2022) the tool can be used as a GUI or from command line / pycharm / etc.

The GUI form of the tool accepts information regarding the folder where a batch of text files are stored. It analyzes each txt file in the folder.

The GUI form also allows the user to select the path and file name for the output file.

Currently (as of 10/28/2022) the main form of the tool outputs a single text file that contains the information for all of the text files in the input path. Sample output looks as follows:


<example output>
*************
Filename: File1.txt

Motion Satellite-Framing Count: 2

Motion Satellite-Framing Examples:
go in ("He went in the room.")
walk through ("He walked through the kitchen.")
run up ("He ran up the hill.")

Motion Verb-Framing Count: 1

Motion Verb-Framing Examples:
enter ("He entered the room.")

Motoin Path Reduplication Count: 1

Motion Path Reduplication Examples:
return back ("He returned back to his house.")

Change of State Satellite-Framing Count: 1

Change of State Satellite-Framing Examples: 
get smaller ("He watched as the pile go smaller")

Change of State Verb-Framing Count: 1

Change of State Verb-Framing Examples: 
died ("He was sad because his friend died.")

Change of State Path Reduplication Count: 0

Change of State Path Reduplication Examples: 

Unsure Satellite-Framing Count: 1

Unsure Satellite-Framing Examples: 
woken up ("It was 3AM when he was woken up by the sound.")


*************
Filename: File2.txt

....
etc.

</end example output>
