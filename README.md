# EventConflationFinder
If you use this tool, please cite:
XXX coming soon

Analyzes text, finds and counts satellite-framed and verb-framed expressions in English (as of 10/28/2022) and Japanese (coming soon). 

The tool distinguishes between motion and change-of-state expressions and further flags expressions that are instances of path reduplication (Spring & Ono, 2014) and expressions that the tool is unsure about. 

Counts, items, and example sentences for checking are output by the tool.

Currently (as of 01/10/2023) the tool can be used as a GUI or from command line / pycharm / etc.

The GUI form of the tool accepts information regarding the folder where a batch of text files are stored. It analyzes each txt file in the folder.

The GUI form also allows the user to select the path and file name for the output file.

Currently (as of 01/10/2023) the main form of the tool allows users to select the form of the output. 
Selecting "Full Data" outputs a single text file that contains the information for all of the text files in the input path including counts of different types of events, the specific event forms and the sentences from which they were taken. 
This mode also includes all "unsure" examples and is therefore the best mode for a robust qualitative analysis. Sample output looks as follows:


<example output for "Full_Data"> 
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

 Selecting "Just Numbers" outputs a single CSV file that contains the numerical information for all of the text files in the input path including counts of different types of events and percentages. 
 It does not include "unsure" events and is therefore only appropriate for generalizations of big-data. 
 The numbers and percentages provided (and their calculations) are as follows:

filename: (name of text file analyzed)
SF_Motion_Count: count of all "sure" instances of satellite-framed motion events
VF_Motion_Count: count of all "sure" instances of satellite-framed motion events
Path_Redup_Motion: count of all "sure" instances of path-reduplicated motion events (e.g., "exit out of the room")
SF_Change_Count: count of all "sure" instances of satellite-framed change-of-state events
VF_Change_Count: count of all "sure" instances of verb-framed change-of-state events
Path_Redup_Change: count of all "sure" instances of path-reduplicated change-of-state events (e.g., "assemble together")
SF_Other_Count: count of all "sure" instances of satellite-framed "other" events (i.e., "realization of goals", "correlatoin of activities", and "aspect")
%SF_Motion: SF_motion / (SF_motion + VF_motion + PR_motion)
%SF_Change: SF_change / (SF_change + VF_change + PR_change)
%SF_Change_and_Other: (SF_change + SF_other) / (SF_change + SF_other + VF_change + PR_change) 
%SF_Motion_and_Change: (SF_motion + SF_change) / (SF_motion + SF_change + VF_motion + VF_change + PR_motion + PR_change)
%SF_Overall: (SF_motion + SF_change + SF_other) / (SF_motion + SF_change + SF_other + VF_motion + VF_change + PR_motion + PR_change)

