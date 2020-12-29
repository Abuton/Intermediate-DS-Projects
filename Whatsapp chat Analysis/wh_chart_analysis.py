import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import plotly.express as px
import string
from wordcloud import WordCloud

plt.style.use('ggplot')
st.set_option('deprecation.showPyplotGlobalUse', False)

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


def draw_wordcloud(msgs):
# word cloud visualization

    allWords = ' '.join([twts for twts in msgs])
    wordCloud = WordCloud(width=300, height=150, random_state=21, max_words=200, mode='RGBA',
                        max_font_size=140, stopwords=stopwords, scale=9,
                          min_word_length=4).generate(allWords)
    plt.figure(figsize=(18, 10))
    plt.imshow(wordCloud, interpolation="bilinear")
    plt.axis('off')
    plt.tight_layout(); plt.title('most used words', size=20)
    plt.savefig('masked_wordcloud.jpg')
    plt.show()

def text_process(mess):
  """
  Takes in a string of text, then performs the following:
  1. Remove all punctuation
  2. Remove all stopwords
  3. Returns a list of the cleaned text
  """
  # Check characters to see if they are in punctuation
  nopunc = [char for char in mess if char not in string.punctuation]

  # Join the characters again to form the string.
  nopunc = ''.join(nopunc)
  
  # Now just remove any stopwords
  clean_message = [word.lower() for word in nopunc.split() if word.lower() not in stopwords]
  return ' '.join(clean_message)

def read_file(file):
  """
  reads whatsapp text file into a list of strings
  """
  x = open(file, 'r+', encoding='utf-8')
  y = x.read()
  content = y.splitlines()
  return content

 #removing emojis
def remove_emoji(text):
  return text.encode('ascii', 'ignore').decode('ascii')
def word_count(s):
    return len(s.split())

def pie_chart(user):
  fig, ax = plt.subplots(figsize=(15, 8))
  explodex = []
  for i in np.arange(len(user)):
      explodex.append(0.005)
  ax = user.plot(kind='pie', colors=['red', 'green', 'cyan', 'lime', 'gold'], fontsize=12, autopct='%1.1f%%', startangle=180,
                pctdistance=0.85, explode=explodex)
  inner_circle = plt.Circle((0,0), 0.50, fc='white')
  fig = plt.gcf()
  fig.gca().add_artist(inner_circle)
  ax.axis('equal')
  ax.set_title('Distribution of User with charts', fontsize=20)
  plt.tight_layout()
  plt.show()

def upload_data():
	st.subheader('Chat Analysis')
	st.write('Upload the chat dataset to get the Analysis')

	try:
		uploaded_file = st.file_uploader('Whatsapp chat dataset', type='txt')
		if uploaded_file:
			st.write('file uploaded successfully :joy: ' )
			wh_chat = pd.read_csv(uploaded_file, sep='\t', header=None)[0].tolist()
			msgs = [] #message container
			pos = 0 
			for line in wh_chat:
				if re.findall("\A\d+[/]", line):
					msgs.append(line)
					pos += 1
				else:
					take = msgs[pos - 1] + ". "+ line
					msgs.append(take)
					msgs.pop(pos -1)
				# extract time
				time = [msgs[i].split(',')[-1].split('-')[0] for i in range(len(msgs))]
				time =  [s.strip(' ') for s in time]
				# extract date
				date = [msgs[i].split(',')[0] for i in range(len(msgs))]
				# extract user
				name = [msgs[i].split('-')[1].split(':')[0] for i in range(len(msgs))]
				# extract msgs (content)
				content = []
				for i in range(len(msgs)):
				  try:
				    content.append(msgs[i].split(':')[2])
				  except IndexError:
				    content.append('Missing Text')
		  # convert to dataframe
			df = pd.DataFrame(list(zip(date, time, name, content)), columns = ['Date', 'Time', 'Sender', 'Content'])
			# drop
			df.drop(0, axis=0, inplace=True)
			st.write(f'There are {df.shape[0]} messages')
			# drop the media
			df = df[df['Content'] != ' <Media omitted>']
			# remove all emoji
			df['Content'] = df['Content'].apply(remove_emoji)
			# add the chat length
			df['chat_length'] = df['Content'].apply(len)
			# add word count
			df['word_count'] = df['Content'].apply(word_count)
			# convert date to a datetime obj
			df['Date'] = pd.to_datetime(df['Date'])
			# extract day,month,year
			df['day_name'] = df['Date'].dt.day_name()
			df['month_name'] = df['Date'].dt.month_name()
			df['year'] = df['Date'].dt.year
			# map the month and day
			st.dataframe(df.head(20))

		  # which sender sends the most message??
			df.Sender.value_counts().head(25).plot(kind='bar', figsize=(13,7), title='Message Distribution amongest Senders')
			plt.xlabel('Sender', fontsize=13);plt.ylabel('Message Count', fontsize=13); plt.xticks(rotation=0, fontsize=14);plt.show()
			st.pyplot()

			# chart length
			df.chat_length.plot.hist(bins=70, figsize=(14, 7), title='chat length distribution')
			plt.xlabel('Chat character counts', fontsize=13);plt.show()
			st.pyplot()

			# Average per user?
			top25_user = df['Sender'].value_counts().index[:25]
			for i in top25_user:
			  st.write(f"Average character per message for sender {i} is , {df[df['Sender'] == i]['chat_length'].mean().round(2)}")

			st.write('Top User chat by Month')
			df[df['Sender']==top25_user[0]].hist(column='chat_length', by='month_name', bins=50, figsize=(18,7));
			st.pyplot()

			expander1 = st.beta_expander("how many msgs are sent on a monthly basis?")
			st.write("")
			expander1.dataframe(pd.DataFrame(df.groupby('month_name')['month_name'].count().sort_values(ascending=False)).rename(columns={'month_name':'msg_count'}))

			expander2 = st.beta_expander("how many msgs per day")
			expander2.dataframe(pd.DataFrame(df.groupby('day_name')['day_name'].size().sort_values(ascending=False)).rename(columns={'day_name':'msg_count'}))

			expander3 = st.beta_expander("per year and month distribution of msgs")
			expander3.dataframe(pd.DataFrame(df.groupby(['year', 'month_name'])['day_name'].size().sort_values(ascending=False)).rename(columns={'day_name':'msg_count'}))

			date_with_high_traffic = pd.DataFrame(df.groupby('Date')['Date'].count()).rename(columns={'Date':'msg_count'})
			# st.write(date_with_high_traffic)
			ax = px.line(date_with_high_traffic, x=date_with_high_traffic.index, y='msg_count', width=950, height=550,
							title='Timeline Trend of chats')
			st.plotly_chart(ax)

			expander4 = st.beta_expander('Montly chat record ')
			month_per_msg = df.groupby('month_name')['month_name'].count().reset_index(name='msg_count')
			expander4.write(month_per_msg)

			fig = px.pie(month_per_msg, values='msg_count', labels='month_name', width=900, height=700, hole=.3,
			 						hover_data=['month_name'])
			# fig.update_traces(textposition='inside', textinfo='label+percent', labelinfo='label')
			fig.update_layout(showlegend=False, yaxis={'visible':False}, title='Montly Chat Record')
			st.plotly_chart(fig)

			st.write('Daily Chat Plot')
			active_hr = df.groupby('day_name')['day_name'].count().reset_index(name='msg_count')
			fig = px.pie(active_hr, values='msg_count', labels='day_name', width=900, height=700, hover_data=['day_name'])
			st.plotly_chart(fig)

			# This will take a while to complete, you can go grab some snack or do some chores
			df['clean_content'] = df['Content'].apply(text_process)
			expander5 = st.beta_expander('Check the clean data?')
			expander5.dataframe(df.head(20))

			draw_wordcloud(df['clean_content'])
			st.pyplot()

			st.balloons()
	except:
		st.warning('Please Upload a txt file')

if __name__ == '__main__':
	upload_data()