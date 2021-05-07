from Core.DownloadFiles import DownloadFiles
from Core.AudioSentimentAnalyzer import AudioSentimentAnalyzer
from Core.TextSentimentAnalyzer import TextSentimentAnalyzer
import Core.RiskAssesment as risk_level
from Core.SpeechToText import Transcribe
from Core.Pyannote import SpeakerDiarization

from Core.Gui import entry
# from Core.Gui.entry import loginPage
# from Core.Gui import Vi
from collections import Counter

from Core.DownloadFiles import DownloadFiles 
from random import randint
from Core.Encode_decode import Encryption

import time
import os
import glob

if __name__ == '__main__':
    
    search_files = True
    delete_files = True
    encryption = True

    seconds =  time.time()
    local_time = time.ctime(seconds)
    print('System Started at: {}'.format(local_time))
    download_files = DownloadFiles('1NEgeaDI7H5N9rvJekEVsw7IrPz-73zNK')
    while search_files:
        files = download_files.search_files()
        if files == 0:
            download_files.download_files()
            cfname = download_files.move_files()
            # print('New search started after threat detection')

            

            if delete_files == True:
                if os.path.exists('./Data/transcription.txt'):
                    os.remove('Data/transcription.txt')
                    print('transcription.txt is deleted')
                else:
                    print('transcription.txt does not exists, will be created as the program runs')
                
                if os.path.exists('./Data/diarization.txt'):
                    os.remove('Data/diarization.txt')
                    print('diarization.txt is deleted')
                else:
                    print('diarization.txt does not exists, will be created as the program runs')
                files = glob.glob('./Data/Trimmed_Audio/*')
                for f in files:
                    person = glob.glob(f+'/*')
                    for file in person:
                        os.remove(file)

            #Speaker Dirazation
            speakerdiarization = SpeakerDiarization('./Data/cloudFiles/'+cfname, './Data/diarization.txt')
            speakerdiarization.run()
            speakerdiarization.sel()
            file_details = speakerdiarization.trim()
            call_duration = speakerdiarization.audio_duration()
            print(file_details)



            # Download files from google Drive
            # download_files = DownloadFiles('1NEgeaDI7H5N9rvJekEVsw7IrPz-73zNK')
            # download_files.search_files()
            # download_files.download_files()

            #text tospeech
            transcribe = Transcribe(folder_name = './Data/Trimmed_Audio', text_file = './Data/transcription.txt')
            

            # Audio sentiment analysis

            audiosentimentanalyzer = AudioSentimentAnalyzer()
            audiosentimentanalyzer.load_model()
            audio_emotions_p1 = []
            audio_emotions_p2 = []
            total_audio_emotions = []
            for dirpath, dirname, filenames in os.walk('./Data/Trimmed_Audio'):
                for file in filenames:
                    # print(dirpath)
                    # print(dirname)
                    print(str(file))
                    audio_prediction = audiosentimentanalyzer.predict(dirpath+'/'+file)
                    speaker_text = transcribe.return_text(dirpath+'/'+file)
                    file_details[file].append(audio_prediction)
                    file_details[file].append(speaker_text)
                    print('File name:{} '.format(file))
                    print('Speaker: {} '.format(file_details[file][3]))
                    print('Start: {}  End: {}'.format(file_details[file][0],file_details[file][1]))
                    print('Duration: {} '.format(file_details[file][2]))
                    print('Predicted emotion: {}'.format(file_details[file][4]))
                    print('What Speaker is saying: {}'.format(file_details[file][5]))
                    print('----------------------------------------------')
                    if file_details[file][3] == 'person1':
                        audio_emotions_p1.append(audio_prediction)
                    elif file_details[file][3] == 'person2':
                        audio_emotions_p2.append(audio_prediction)
                    total_audio_emotions.append(audio_prediction)

        

            # Text Sentiment analysis

            textsentimentanalyzer = TextSentimentAnalyzer(transcript= './Data/transcription.txt')
            threat_words =  textsentimentanalyzer.find_emotion(emotion_file = './Data/emotions.txt')
            # textsentimentanalyzer.SentimentAnalyzer()
            print('Threat Words Detected: {}'.format(threat_words))
            no_of_threat_keys = textsentimentanalyzer.plotAnalysis()
            print('no of threat keys {}'.format(no_of_threat_keys))
            print('____________________________')


            def temp(audio_emotions):
                division = []
                w = Counter(audio_emotions)
                total = sum(w.values())
                print('Division of emotions')
                for key in w.keys():
                    emotion_percent = round((w[key]/total*100),2)
                    string  = str(key)+': '+str(emotion_percent)+'%'
                    division.append(string)
                    # print('{}: {}%'.format(key, emotion_percent))
                    # print('_________________')
                return list(w.keys())[list(w.values()).index(max(w.values()))], division
            # print(final_audio_prediction)
            print('Person1 Division of emotions')
            print(audio_emotions_p1)
            print('--------------------------------------------------------------')
            
            print('Person2 Division of emotions')
            print(audio_emotions_p2)
            print('--------------------------------------------------------------')
            try:    
                p1, person1_divison_emotions = temp(audio_emotions_p1)
                print(person1_divison_emotions)
                print('----------------------------')
                p2, person2_divison_emotions = temp(audio_emotions_p2)
                print(person2_divison_emotions)
                print('Person1 Emotions:{} ==== Person2 Emotions:{}'.format(p1,p2))
            except ValueError:
                person2_divison_emotions = '0'
                pass
            # print('----------------------------')
            # print('Final Analysis')

            try:    
                p1_risk_level = risk_level.audio_risk_assesment(no_threat_keys= no_of_threat_keys,list_audio_threat= audio_emotions_p1)
                print('Total risk level in Conversation of Person 1: {}%'.format(p1_risk_level))
                print('____________________________________________________')
                p2_risk_level = risk_level.audio_risk_assesment(no_threat_keys= no_of_threat_keys,list_audio_threat= audio_emotions_p2)
                print('Total risk level in Conversation Person 2: {}%'.format(p2_risk_level))
                print('____________________________________________________')
            except ValueError:
                pass

            final_risk_level = risk_level.overall_risk_assesment(no_threat_keys= no_of_threat_keys,list_audio_threat= total_audio_emotions)
            print('Total risk level in Conversation: {}%'.format(final_risk_level))

            
        # Random Phone number generator
            phonenumbers = []
            def random_with_N_digits(n):
                range_start = 10**(n-1)
                range_end = (10**n)-1
                return randint(range_start, range_end)

            for mciNumbers in range(0,2):
            #     print('912{}'.format(random_with_N_digits(7)))
                number = '912{}'.format(random_with_N_digits(7))
                phonenumbers.append(number)


            if encryption:
                encryptor = Encryption('Core/encryption_key.key')
                encryptor.load_key()
                for dirpath, dirname, filenames in os.walk('Data/Trimmed_Audio'):
                    for file in filenames:
                        print(dirpath+'/'+file)
                        encryptor.encrypt(dirpath+'/'+file, '.enc')

                encryptor.encrypt('E:/Programming/Call Surveillance/Data/cloudFiles/'+cfname, '.enc')
                encryptor.encrypt('Data/diarization.txt', '.enc')
                encryptor.encrypt('Data/transcription.txt', '.enc')

            #Gui & Database
            # result = entry.connect_database()

            if final_risk_level > 50:
                entry.insert(phonenumbers[0], phonenumbers[1], str(no_of_threat_keys), str(final_risk_level), 'Open', 
                str(threat_words).replace('[','').replace(']','').replace("'","").replace(',', '|').strip(),
                str(person1_divison_emotions).replace('[','').replace(']', '').replace("'","").replace(',', '|'),
                str(person2_divison_emotions).replace('[','').replace(']', '').replace("'","").replace(',', '|'), 
                call_duration)
                time.sleep(20)
                continue

        else:
            seconds =  time.time()
            local_time = time.ctime(seconds)
            # print("Local time:", local_time)
            print('New search started at: {}'.format(local_time))
            time.sleep(15)
            continue

    # angry + happy -> 2
    # Calm + neutral
# dd887dn
