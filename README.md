# Psychological Safety Dataset

Based on [AMI Corpus](https://groups.inf.ed.ac.uk/ami/corpus/), this dataset contains annotations on the specific utterances that would affect the psychological safety of the meeting participants.

## Coverage

The current version of the dataset contains annotations covering following sessions from AMI Corpus:

- ES2004(a-d)
- ES2005(a-d)
- ES2006(a-d)
- ES2007(a-d)
- ES2008(a-d)

The current version of the dataset also contains annotations partially covering the following sessions from AMI Corpus:

- ES2009a (- 960s)
- ES2009b (- 720s)
- ES2009c (- 720s)
- ES2009d (- 840s)
- ES2010a (- 360s)
- ES2010b (- 600s)
- ES2010c (- 240s)
- ES2010d (- 240s)

Every annotated meeting is about designing a remote control based on a scenario. You can find more details about the meetings from AMI Corpus documentation.

## Pre-processing corpus

The AMI corpus stores the utterances of the participants in word level. To aggregate the words in terms of the sentences, a separate Python script (```transcript-parser.py```) was used. To use the script, place the AMI Corpus files as following.

- amicorpus
  - words
    - EN2001a.A.words.xml
    - ...
- transcript_parser.py

Then, change the list ```fileIDs``` in the script to process the meetings of interest, and run the script. The script is compatible with Python 3.8 and 3.9.

## Annotation Structure

Annotations for each meeting is stored as a separate csv file, named as ```(meeting-ID)-moments.csv```. Each row contains the annotation with the following fields:

- user_id: Anonymized annotator ID. It keeps the consistent value across multiple meetings
- dataset: ID of the dataset
- timestamp: The time when the annotated utterance was made within the meeting.
- speaker: The ID of the speaker, given as in AMI Corpus.
- line: The actual content of the utterance.
- direction: ```POSITIVE``` if the annotator decided that the annotated line reinforces the psychological safety of the group, and ```NEGATIVE``` if she decided that the line harms the psychological safety of the group.
- agree_cnt: The number of annotations that agrees on the ```direction```
- reason: The reason why the annotator thought the line would affect the psychological safety of the group.
- possible_comment: The comment of the annotator. It is written as if the annotator is giving feedback to the speaker of the utterance.
- created_at: The time when the annotation was submitted.
