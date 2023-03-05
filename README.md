# IRONHACK Repository
This is the project what I created for my Final Bootcamp project in Data Analytics in [IronHack](http://www.ironhack.com).
The idea was to try to improve the Bootcamp experience, adquiring more students and helping to the existing students. So I decided to transcribe all the videos of my bootcamp, captioning them, creating an summary and keywords, all automatic (at this moment, couldn't finish all the automatism but exists all the functions for that).

The project also include one app to search and find videos about one topic (or any word you want to use in any language that was translated) and when decide the video you want to explore have the option to search inside the video and locate the exact moment where the video talk about your searching (Future feature, continue the implementing of the FULL TEXT index in MySQL with the option of Natural Language).

To play the videos with subtitles and locate in the exact position I used [VLC media player](https://www.videolan.org/vlc/index.es.html).

I would wanted to train my own models but my hardware and the time made me to change my mind, however this project is not closed so maybe in the future I return here to improve it.

## Process

- ### Transcription
For this task I decided to use [Whisper](https://github.com/openai/whisper). After testing different options, this was which fitted more to my project. I used the model "base.en" because of my schedule (I had to create the project after work) and hardware requirements but can use other larger to get better performance, or even multi-language.
- ### Subtitles
I had many problems to manage the subtitles, I tried to split the videos but synchronize again the subtitles was impossible with the time I had to do it, so at the end I decided to use [Stable Whisper](https://github.com/jianfch/stable-ts) without split the video.
- ### Summary
This task I decided to use [Hugging Face transformers](https://huggingface.co/docs/transformers/index) after try other options, I also tried many different models and decided to use **mrm8488/flan-t5-large-finetuned-openai-summarize_from_feedback** which gave me better results.
- ### Keywords
[KeyBERT](https://maartengr.github.io/KeyBERT/) was the chosen between some alternatives and the model I used was **https://tfhub.dev/google/universal-sentence-encoder/4**
- ### Translation
This was the only part that didn't tried other options because I used it before and worked fine to me but this also was not a smooth path, beware that translating subtitles can you give you some surprises (break lines...) so I decided to split the subtitles in lines and translate them to joined together at the end.
- ### BBDD
This process store in one MySQL database all the texts I got (originals and translations) with the relationship with the videos. I created FULL TEXT index in the database bud needed to delete them because took more time to do the process so I will implement this in the future with better searching.
- ### APP
Since I tried Flask in my [Mid Bootcamp project](https://github.com/oiroqueiro/mid-bootcamp-project), for this project I wanted to try any other options and after research about Streamlit and Django, I decided to take the complicated path, so I used Django (with Bootstrap 5).

As I said before, the limited time didn't allowed me to finish everything I had in my mind (launch all the logic from Django, update videos, option to transcribe online videos (at the moment only can use files).

