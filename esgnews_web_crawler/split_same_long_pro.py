import sqlite3
import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


conn = sqlite3.connect('D:\\nlp_project_data\\esgnews\\output_same_long.db')
cur = conn.cursor()
cur.execute("select * from OUTPUTS")
datas = cur.fetchall()
conn.commit()
conn.close()
for data in datas:
    words = nltk.word_tokenize(data[0])
    # lowercasing each token
    words = [token.lower() for token in words]
    # stemming
    port = PorterStemmer()
    stemmed_port = [port.stem(token) for token in words]

    lanc = LancasterStemmer()
    stemmed_lanc = [lanc.stem(token) for token in words]

    snow = SnowballStemmer("english")
    stemmed_snow = [snow.stem(token) for token in words]
    ways = [{'class': 'port', 'name': stemmed_port}, {'class': 'lanc',
                                                      'name': stemmed_lanc}, {'class': 'snow', 'name': stemmed_snow}]
    for way in ways:
        conn = sqlite3.connect(
            'D:\\nlp_project_data\\esgnews\\output_same_long_'+way['class']+'.db')
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS OUTPUTS ('text' TEXT PRIMARY KEY,'ESGtag' TEXT)")
        tags = nltk.pos_tag(way['name'])
        result = []

        lemmatiser = WordNetLemmatizer()
        for tag in tags:
            wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
            result.append(lemmatiser.lemmatize(tag[0], pos=wordnet_pos))
        # defining stopwords in English
        stop_words = set(stopwords.words("english"))
        # removing stop words
        words_no_stop = [word for word in result if word not in stop_words]
        sentence = ''
        for word in words_no_stop:
            sentence += word+' '
        cur.execute("Insert or ignore into OUTPUTS Values(?,?)",
                    (sentence, data[1]))
        conn.commit()
        conn.close()
