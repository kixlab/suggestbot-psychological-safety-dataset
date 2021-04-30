import re
from html.parser import HTMLParser
import html
# from HTMLParser import HTMLParser
import csv
import json

h = HTMLParser()


def combineScript(fileID, speakerIDs):
    totalLines = []
    for j in range(len(speakerIDs)):
        speakerID = speakerIDs[j]
        f = open('./amicorpus/words/' + fileID +
                 '.' + speakerID + '.words.xml', "r")
        txt = f.read()
        lines = txt.split("\n")
        for i in range(1, len(lines) - 1):
            word_obj = {"speaker": speakerID,
                        "starttime": 0, "endtime": 0, "word": ""}
            word_search = re.search(
                '<w .* starttime="(.*)" endtime="(.*)">(.*)</w>', lines[i], re.IGNORECASE)
            disf_search = re.search(
                '<disfmarker (.*) starttime="(.*)" endtime="(.*)"/>', lines[i], re.IGNORECASE)
            gap_search = re.search(
                '<gap .* starttime="(.*)" endtime="(\d*\.?\d*)"/>', lines[i], re.IGNORECASE)
            sound_search = re.search(
                '<vocalsound .* starttime="(.*)" endtime="(.*)" type="(.*)"/>', lines[i], re.IGNORECASE)
            error = re.search(
                '<transformerror (.*) starttime="(.*)" endtime="(.*)"/>', lines[i], re.IGNORECASE)
            if word_search:
                word_obj['starttime'] = float(word_search.group(1))
                word_obj['endtime'] = float(word_search.group(2).split('"')[0])
                word_obj['word'] = html.unescape(word_search.group(3))
                if(word_obj['word'] in ['.', ',', '!', '?']):
                    totalLines[len(totalLines) - 1]['word'] += word_obj['word']
                    totalLines[len(totalLines) -
                               1]['endtime'] = word_obj['endtime']
                elif(len(totalLines) > 0 and totalLines[len(totalLines) - 1]['word'].endswith(('>', '.', '!', '?'))):
                    totalLines.append(word_obj)
                elif(len(totalLines) > 0 and word_obj['starttime'] == totalLines[len(totalLines) - 1]['endtime']):
                    totalLines[len(totalLines) - 1]['word'] = totalLines[len(
                        totalLines) - 1]['word'] + ' ' + word_obj['word']
                    totalLines[len(totalLines) -
                               1]['endtime'] = word_obj['endtime']
                else:
                    totalLines.append(word_obj)
            elif gap_search:
                word_obj['starttime'] = float(gap_search.group(1))
                word_obj['endtime'] = float(gap_search.group(2))
                word_obj['word'] = "<gap>"
                totalLines.append(word_obj)
            elif sound_search:
                word_obj['starttime'] = float(sound_search.group(1))
                word_obj['endtime'] = float(sound_search.group(2))
                word_obj['word'] = "<sound: " + sound_search.group(3) + ">"
                totalLines.append(word_obj)
            elif error:
                word_obj['starttime'] = float(error.group(2))
                word_obj['endtime'] = float(error.group(3))
                word_obj['word'] = "<error>"
                totalLines.append(word_obj)
            else:
                print(lines[i])

    sorted_totalLines = sorted(totalLines, key=lambda k: k['starttime'])
    # for x in range(len(sorted_totalLines)-1):
    #   print(sorted_totalLines[x])
    return sorted_totalLines


def processPunc(lists, lines):
    i = len(lists)-1
    while ((lists[i]['speaker'] != lines['speaker'])):
        i -= 1
    lists[i]['text'] += lines['word']
    return lists


def makeTranscript(lines):
    transcript = []

    for i in range(len(lines)):
        # if(i == 0 or lines[i]['speaker'] != lines[i-1]['speaker'] or lines[i-1]['word'].endswith(('.', '!', '?'))):
        trans_obj = {"speaker": "", "starttime": 0,
                      "endtime": 0, "text": ""}
        trans_obj['speaker'] = lines[i]['speaker']
        trans_obj['starttime'] = lines[i]['starttime']
        trans_obj['endtime'] = lines[i]['endtime']
        trans_obj['text'] = lines[i]['word']
        transcript.append(trans_obj)
        # else:
        #     trans_obj = transcript.pop()
        #     trans_obj['text'] += ' '
        #     trans_obj['text'] += lines[i]['word']
        #     trans_obj['endtime'] = lines[i]['endtime']
        #     transcript.append(trans_obj)

    return transcript


fileIDs = ['ES2009a', 'ES2009b', 'ES2009c', 'ES2009d', 'ES2010a', 'ES2010b', 'ES2010c', 'ES2010d'] ## Change the meeting IDs here.


for fileID in fileIDs:
    # fileID = "ES2016a"
    speakerIDs = ["A", "B", "C", "D"]
    transcript = makeTranscript(combineScript(fileID, speakerIDs))

    with open(fileID + '_combined.json', 'w') as json_file:
        json.dump(transcript, json_file, indent=4)

# with open('./transcripts/' + fileID + 'test', 'w') as csvfile:
#         writer = csv.writer(csvfile, delimiter="\t", quotechar='"')
#         for i in range(len(transcript)):
#                 writer.writerow([transcript[i]['starttime'], transcript[i]['endtime'],
#                                  '( ' + transcript[i]['speaker'] + ' )', transcript[i]['text']])
# print(sorted_transcript)
